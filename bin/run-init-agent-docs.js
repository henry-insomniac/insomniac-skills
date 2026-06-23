const { spawnSync } = require("node:child_process");
const path = require("node:path");

function runInitAgentDocs(args) {
  const scriptPath = path.resolve(__dirname, "..", "scripts", "init_agent_docs.py");
  const result = spawnSync("python3", [scriptPath, ...args], { stdio: "inherit" });

  if (result.error) {
    if (result.error.code === "ENOENT") {
      console.error("python3 is required to run init-agent-docs.");
      return 1;
    }

    console.error(result.error.message);
    return 1;
  }

  return result.status ?? 1;
}

module.exports = { runInitAgentDocs };
