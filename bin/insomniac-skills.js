#!/usr/bin/env node

const { runInitAgentDocs } = require("./run-init-agent-docs");

function printHelp() {
  console.log(`Usage: insomniac-skills <command> [options]

Commands:
  init               Short alias for init-agent-docs.
  init-agent-docs    Initialize reusable Agent collaboration docs.

Examples:
  isk init --name my-project
  isk init --name my-project --design --issues --ops
  insomniac-skills init --name my-project

The direct command is also available:
  init-agent-docs [options]`);
}

const args = process.argv.slice(2);
const [command, ...rest] = args;

if (!command || command === "-h" || command === "--help") {
  printHelp();
  process.exit(0);
}

if (command === "init" || command === "init-agent-docs" || command === "init_agent_docs") {
  process.exit(runInitAgentDocs(rest));
}

if (command.startsWith("-")) {
  process.exit(runInitAgentDocs(args));
}

console.error(`Unknown command: ${command}`);
console.error('Run "insomniac-skills --help" for usage.');
process.exit(1);
