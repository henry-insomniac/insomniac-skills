#!/usr/bin/env sh
set -eu

TOOL_NAME="init-agent-docs"
BASE_URL="${INSOMNIAC_SKILLS_BASE_URL:-https://yi-flow.com/insomniac-skills}"
TARBALL_URL="${INSOMNIAC_SKILLS_TARBALL_URL:-$BASE_URL/insomniac-skills.tar.gz}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "python3 is required but was not found." >&2
  exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
  INSTALL_DIR="${INSOMNIAC_SKILLS_INSTALL_DIR:-/opt/insomniac-skills}"
  BIN_DIR="${INSOMNIAC_SKILLS_BIN_DIR:-/usr/local/bin}"
else
  DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
  INSTALL_DIR="${INSOMNIAC_SKILLS_INSTALL_DIR:-$DATA_HOME/insomniac-skills}"
  BIN_DIR="${INSOMNIAC_SKILLS_BIN_DIR:-$HOME/.local/bin}"
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

download() {
  url="$1"
  dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$dest"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$dest" "$url"
  else
    echo "curl or wget is required to download $url." >&2
    exit 1
  fi
}

case "$INSTALL_DIR" in
  *insomniac-skills*) ;;
  *)
    echo "Refusing to install into unsafe path: $INSTALL_DIR" >&2
    exit 1
    ;;
esac

echo "Downloading $TOOL_NAME from $TARBALL_URL"
download "$TARBALL_URL" "$TMP_DIR/insomniac-skills.tar.gz"

mkdir -p "$TMP_DIR/package" "$INSTALL_DIR" "$BIN_DIR"
tar -xzf "$TMP_DIR/insomniac-skills.tar.gz" -C "$TMP_DIR/package"

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -R "$TMP_DIR/package/." "$INSTALL_DIR/"

chmod +x "$INSTALL_DIR/scripts/init_agent_docs.py"
ln -sf "$INSTALL_DIR/scripts/init_agent_docs.py" "$BIN_DIR/init-agent-docs"
ln -sf "$INSTALL_DIR/scripts/init_agent_docs.py" "$BIN_DIR/init_agent_docs"

"$PYTHON_BIN" -m py_compile "$INSTALL_DIR/scripts/init_agent_docs.py"
rm -rf "$INSTALL_DIR/scripts/__pycache__"
"$BIN_DIR/init-agent-docs" --help >/dev/null

echo "$TOOL_NAME installed:"
echo "  install dir: $INSTALL_DIR"
echo "  command:     $BIN_DIR/init-agent-docs"

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *)
    echo "Warning: $BIN_DIR is not in PATH for this shell."
    echo "Run directly with: $BIN_DIR/init-agent-docs"
    ;;
esac
