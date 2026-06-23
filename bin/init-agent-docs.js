#!/usr/bin/env node

const { runInitAgentDocs } = require("./run-init-agent-docs");

process.exit(runInitAgentDocs(process.argv.slice(2)));
