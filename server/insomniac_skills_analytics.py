#!/usr/bin/env python3
"""Serve insomniac-skills release files and record install analytics."""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import html
import ipaddress
import json
from pathlib import Path
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen


DEFAULT_RELEASE_DIR = Path("/var/www/html/insomniac-skills")
DEFAULT_DB_PATH = Path("/var/lib/insomniac-skills/analytics.sqlite3")
RETENTION_DAYS = 180
MAX_EVENTS = 20000


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                event_type TEXT NOT NULL,
                ip TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                referer TEXT NOT NULL,
                country TEXT NOT NULL DEFAULT '',
                region TEXT NOT NULL DEFAULT '',
                city TEXT NOT NULL DEFAULT '',
                isp TEXT NOT NULL DEFAULT ''
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ip_geo_cache (
                ip TEXT PRIMARY KEY,
                country TEXT NOT NULL DEFAULT '',
                region TEXT NOT NULL DEFAULT '',
                city TEXT NOT NULL DEFAULT '',
                isp TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            )
            """
        )


def client_ip(headers: dict[str, str], fallback: str) -> str:
    for header in ("CF-Connecting-IP", "X-Real-IP", "X-Forwarded-For"):
        value = headers.get(header)
        if not value:
            continue
        ip = value.split(",", 1)[0].strip()
        if ip:
            return ip
    return fallback


def geo_for_ip(db_path: Path, ip: str) -> dict[str, str]:
    empty = {"country": "", "region": "", "city": "", "isp": ""}
    try:
        parsed = ipaddress.ip_address(ip)
    except ValueError:
        return empty
    if parsed.is_private or parsed.is_loopback or parsed.is_link_local:
        return {**empty, "country": "Private"}

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT country, region, city, isp FROM ip_geo_cache WHERE ip = ?",
            (ip,),
        ).fetchone()
        if row:
            return {
                "country": row[0],
                "region": row[1],
                "city": row[2],
                "isp": row[3],
            }

    url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp"
    try:
        with urlopen(url, timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, json.JSONDecodeError):
        return empty

    if payload.get("status") != "success":
        return empty

    geo = {
        "country": str(payload.get("country") or ""),
        "region": str(payload.get("regionName") or ""),
        "city": str(payload.get("city") or ""),
        "isp": str(payload.get("isp") or ""),
    }
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO ip_geo_cache (ip, country, region, city, isp, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(ip) DO UPDATE SET
                country = excluded.country,
                region = excluded.region,
                city = excluded.city,
                isp = excluded.isp,
                updated_at = excluded.updated_at
            """,
            (ip, geo["country"], geo["region"], geo["city"], geo["isp"], utc_now()),
        )
    return geo


def record_event(
    db_path: Path,
    event_type: str,
    ip: str,
    user_agent: str,
    referer: str,
) -> None:
    geo = geo_for_ip(db_path, ip)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO events (
                created_at, event_type, ip, user_agent, referer,
                country, region, city, isp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                utc_now(),
                event_type,
                ip,
                user_agent,
                referer,
                geo["country"],
                geo["region"],
                geo["city"],
                geo["isp"],
            ),
        )
        cutoff = (
            dt.datetime.now(dt.UTC) - dt.timedelta(days=RETENTION_DAYS)
        ).replace(microsecond=0).isoformat()
        conn.execute("DELETE FROM events WHERE created_at < ?", (cutoff,))
        conn.execute(
            """
            DELETE FROM events
            WHERE id NOT IN (
                SELECT id FROM events
                ORDER BY id DESC
                LIMIT ?
            )
            """,
            (MAX_EVENTS,),
        )


def load_stats(db_path: Path) -> dict[str, object]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT created_at, event_type, ip, user_agent, country, region, city, isp
            FROM events
            ORDER BY id DESC
            LIMIT 500
            """
        ).fetchall()

    events = [dict(row) for row in rows]
    installs = [row for row in events if row["event_type"] == "install"]
    packages = [row for row in events if row["event_type"] == "package"]
    countries = Counter((row["country"] or "Unknown") for row in installs)
    cities = Counter(
        ", ".join(part for part in (row["city"], row["region"], row["country"]) if part)
        or "Unknown"
        for row in installs
    )
    days = Counter(row["created_at"][:10] for row in installs)
    return {
        "events": events[:100],
        "total_installs": len(installs),
        "total_packages": len(packages),
        "unique_ips": len({row["ip"] for row in installs}),
        "countries": countries.most_common(12),
        "cities": cities.most_common(12),
        "days": sorted(days.items())[-14:],
    }


def bar_rows(items: list[tuple[str, int]], total: int) -> str:
    if not items:
        return '<p class="muted">No data yet.</p>'
    rows = []
    for label, count in items:
        percent = 0 if total == 0 else max(4, round(count / total * 100))
        rows.append(
            "<div class='bar-row'>"
            f"<span>{html.escape(label)}</span>"
            f"<div class='bar'><i style='width:{percent}%'></i></div>"
            f"<strong>{count}</strong>"
            "</div>"
        )
    return "\n".join(rows)


def mask_ip(ip: str) -> str:
    try:
        parsed = ipaddress.ip_address(ip)
    except ValueError:
        return ip
    if parsed.version == 4:
        parts = ip.split(".")
        return ".".join(parts[:3] + ["x"])
    groups = parsed.exploded.split(":")
    return ":".join(groups[:4]) + "::"


def render_dashboard(db_path: Path) -> bytes:
    stats = load_stats(db_path)
    total = int(stats["total_installs"])
    event_rows = []
    for row in stats["events"]:
        location = ", ".join(
            part for part in (row["city"], row["region"], row["country"]) if part
        ) or "Unknown"
        event_rows.append(
            "<tr>"
            f"<td>{html.escape(row['created_at'])}</td>"
            f"<td>{html.escape(row['event_type'])}</td>"
            f"<td>{html.escape(mask_ip(row['ip']))}</td>"
            f"<td>{html.escape(location)}</td>"
            f"<td>{html.escape(row['isp'] or '')}</td>"
            "</tr>"
        )

    body = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>insomniac-skills analytics</title>
  <style>
    :root {{ color-scheme: light; font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    body {{ margin: 0; background: #f6f7f9; color: #17202a; }}
    header {{ padding: 28px 32px 18px; background: #ffffff; border-bottom: 1px solid #dde2e8; }}
    h1 {{ margin: 0 0 6px; font-size: 26px; letter-spacing: 0; }}
    main {{ padding: 24px 32px 40px; max-width: 1180px; margin: 0 auto; }}
    .muted {{ color: #667085; }}
    .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    .card {{ background: #fff; border: 1px solid #dde2e8; border-radius: 8px; padding: 18px; }}
    .metric {{ font-size: 32px; font-weight: 750; margin-top: 8px; }}
    .charts {{ display: grid; gap: 16px; grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 16px; }}
    .bar-row {{ display: grid; grid-template-columns: 150px 1fr 44px; gap: 10px; align-items: center; margin: 10px 0; }}
    .bar {{ height: 10px; background: #edf1f5; border-radius: 999px; overflow: hidden; }}
    .bar i {{ display: block; height: 100%; background: #2563eb; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #dde2e8; border-radius: 8px; overflow: hidden; }}
    th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #edf1f5; font-size: 14px; }}
    th {{ background: #f0f3f7; font-weight: 650; }}
    section {{ margin-top: 18px; }}
    @media (max-width: 820px) {{ .grid, .charts {{ grid-template-columns: 1fr; }} main, header {{ padding-left: 18px; padding-right: 18px; }} }}
  </style>
</head>
<body>
  <header>
    <h1>insomniac-skills 安装统计</h1>
    <div class="muted">统计 install.sh 调用量、安装包下载量和 IP 归属地。更新时间：{html.escape(utc_now())}</div>
  </header>
  <main>
    <div class="grid">
      <div class="card"><div class="muted">安装脚本调用</div><div class="metric">{stats["total_installs"]}</div></div>
      <div class="card"><div class="muted">安装包下载</div><div class="metric">{stats["total_packages"]}</div></div>
      <div class="card"><div class="muted">独立 IP</div><div class="metric">{stats["unique_ips"]}</div></div>
      <div class="card"><div class="muted">国家/地区数</div><div class="metric">{len(stats["countries"])}</div></div>
    </div>
    <div class="charts">
      <div class="card"><h2>国家/地区</h2>{bar_rows(stats["countries"], total)}</div>
      <div class="card"><h2>城市</h2>{bar_rows(stats["cities"], total)}</div>
      <div class="card"><h2>最近 14 天</h2>{bar_rows(stats["days"], max(total, 1))}</div>
    </div>
    <section>
      <h2>最近事件</h2>
      <table>
        <thead><tr><th>时间 UTC</th><th>类型</th><th>IP</th><th>归属地</th><th>ISP</th></tr></thead>
        <tbody>{''.join(event_rows) or '<tr><td colspan="5">No data yet.</td></tr>'}</tbody>
      </table>
    </section>
  </main>
</body>
</html>"""
    return body.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    release_dir: Path
    db_path: Path

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_bytes(self, content: bytes, content_type: str, cache_control: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", cache_control)
        self.end_headers()
        self.wfile.write(content)

    def send_head_only(
        self, content_length: int, content_type: str, cache_control: str
    ) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(content_length))
        self.send_header("Cache-Control", cache_control)
        self.end_headers()

    def serve_file(self, filename: str, content_type: str, event_type: str) -> None:
        path = self.release_dir / filename
        if not path.is_file():
            self.send_error(404)
            return
        ip = client_ip(dict(self.headers), self.client_address[0])
        record_event(
            self.db_path,
            event_type,
            ip,
            self.headers.get("User-Agent", ""),
            self.headers.get("Referer", ""),
        )
        self.send_bytes(path.read_bytes(), content_type, "no-store")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in ("/install.sh", "/insomniac-skills/install.sh"):
            self.serve_file("install.sh", "text/x-shellscript; charset=utf-8", "install")
            return
        if path in (
            "/insomniac-skills.tar.gz",
            "/insomniac-skills/insomniac-skills.tar.gz",
        ):
            self.serve_file("insomniac-skills.tar.gz", "application/gzip", "package")
            return
        if path in ("/", "/dashboard", "/analytics", "/insomniac-skills/", "/insomniac-skills/dashboard", "/insomniac-skills/analytics"):
            self.send_bytes(render_dashboard(self.db_path), "text/html; charset=utf-8", "no-store")
            return
        self.send_error(404)

    def do_HEAD(self) -> None:
        path = urlparse(self.path).path
        if path in ("/install.sh", "/insomniac-skills/install.sh"):
            file_path = self.release_dir / "install.sh"
            if not file_path.is_file():
                self.send_error(404)
                return
            self.send_head_only(
                file_path.stat().st_size, "text/x-shellscript; charset=utf-8", "no-store"
            )
            return
        if path in (
            "/insomniac-skills.tar.gz",
            "/insomniac-skills/insomniac-skills.tar.gz",
        ):
            file_path = self.release_dir / "insomniac-skills.tar.gz"
            if not file_path.is_file():
                self.send_error(404)
                return
            self.send_head_only(file_path.stat().st_size, "application/gzip", "no-store")
            return
        if path in (
            "/",
            "/dashboard",
            "/analytics",
            "/insomniac-skills/",
            "/insomniac-skills/dashboard",
            "/insomniac-skills/analytics",
        ):
            content = render_dashboard(self.db_path)
            self.send_head_only(len(content), "text/html; charset=utf-8", "no-store")
            return
        self.send_error(404)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18084)
    parser.add_argument("--release-dir", default=str(DEFAULT_RELEASE_DIR))
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    Handler.release_dir = Path(args.release_dir)
    Handler.db_path = Path(args.db)
    init_db(Handler.db_path)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Serving analytics on http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
