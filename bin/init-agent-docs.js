#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const path = require("node:path");

const scriptPath = path.resolve(__dirname, "..", "scripts", "init_agent_docs.py");
const args = [scriptPath, ...process.argv.slice(2)];
const result = spawnSync("python3", args, { stdio: "inherit" });

if (result.error) {
  if (result.error.code === "ENOENT") {
    console.error("python3 is required to run init-agent-docs.");
    process.exit(1);
  }

  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);
