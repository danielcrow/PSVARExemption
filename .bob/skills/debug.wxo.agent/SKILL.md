---
name: debug-wxo-agent
description: Returns traces and logs from the Local Developer Edition of watsonx Orchestrate for recent agent runs. Use this skill to debug watsonx Orchestrate agents (wxo).
---

When asked to debug watsonx Orchestrate agents, use the following commands.

Activate the local virtual Python environment:

"source venv/bin/activate"

Read traces:

"orchestrate observability traces search --last 1h"

Use "orchestrate observability traces export --trace-id <TRACE_ID>" to export 
full trace data for the most recent trace.

Read logs:

"export LIMA_INSTANCE=ibm-watsonx-orchestrate
lima docker logs -f dev-edition-tools-runtime-1
lima docker logs dev-edition-wxo-tempus-runtime-1"

Based on the recent traces and logs identify the most important error, 
describe it and suggest steps how to fix it.