[I 2026-06-01 08:33:06,649.649 mcp_proxy.httpx_client] HTTP Request: POST https://developer.watson-orchestrate.ibm.com/mcp
[I 2026-06-01 08:33:06,649.649 mcp_proxy.httpx_client] Request Headers: {'host': 'developer.watson-orchestrate.ibm.com', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'python-httpx/0.28.1', 'accept': 'application/json, text/event-stream', 'content-type': 'application/json', 'content-length': '152'}
[I 2026-06-01 08:33:07,156.156 httpx] HTTP Request: POST https://developer.watson-orchestrate.ibm.com/mcp "HTTP/1.1 200 OK"
[I 2026-06-01 08:33:07,159.159 mcp.client.streamable_http] Negotiated protocol version: 2025-11-25
[I 2026-06-01 08:33:07,163.163 mcp_proxy.httpx_client] HTTP Request: POST https://developer.watson-orchestrate.ibm.com/mcp
[I 2026-06-01 08:33:07,163.163 mcp_proxy.httpx_client] Request Headers: {'host': 'developer.watson-orchestrate.ibm.com', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'python-httpx/0.28.1', 'accept': 'application/json, text/event-stream', 'content-type': 'application/json', 'mcp-protocol-version': '2025-11-25', 'content-length': '54'}
[I 2026-06-01 08:33:07,170.170 mcp.server.lowlevel.server] Processing request of type ReadResourceRequest
[I 2026-06-01 08:33:07,689.689 httpx] HTTP Request: POST https://developer.watson-orchestrate.ibm.com/mcp "HTTP/1.1 202 Accepted"
[I 2026-06-01 08:33:07,696.696 mcp_proxy.httpx_client] HTTP Request: POST https://developer.watson-orchestrate.ibm.com/mcp
[I 2026-06-01 08:33:07,696.696 mcp_proxy.httpx_client] Request Headers: {'host': 'developer.watson-orchestrate.ibm.com', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'python-httpx/0.28.1', 'accept': 'application/json, text/event-stream', 'content-type': 'application/json', 'mcp-protocol-version': '2025-11-25', 'content-length': '99'}
[I 2026-06-01 08:33:08,210.210 httpx] HTTP Request: POST https://developer.watson-orchestrate.ibm.com/mcp "HTTP/1.1 200 OK"
=== Reading 'orchestrate' Resource ===

---
name: Orchestrate
description: Use when building, testing, and deploying AI agents and tools for watsonx Orchestrate. Reach for this skill when creating native agents, authoring Python or OpenAPI tools, building agentic workflows, managing connections, deploying agents to production, or integrating agents with external systems.
metadata:
    mintlify-proj: orchestrate
    version: "1.0"
---

# watsonx Orchestrate Agent Development Kit (ADK)

## Product summary

The **IBM watsonx Orchestrate Agent Development Kit (ADK)** is a Python library and CLI tool for building and deploying agents and tools to watsonx Orchestrate. Agents are AI-powered entities that use tools, collaborators, and knowledge bases to execute tasks. The ADK enables you to define agents in YAML/JSON/Python, create tools (Python, OpenAPI, agentic workflows, Langflow), manage connections for authentication, and deploy agents across local development, cloud, and on-premises environments.

**Key files and commands:**
- Agent definitions: `agent.yaml`, `agent.json`, or Python classes
- Tool definitions: Python files with `@tool` decorator, OpenAPI specs, or flow definitions
- Connection configs: `connection.yaml` files
- CLI: `orchestrate` command (agents, tools, connections, env, knowledge-bases, etc.)
- Primary docs: https://developer.watson-orchestrate.ibm.com

## When to use

Reach for this skill when:
- **Building agents**: Creating native agents with instructions, tools, collaborators, and knowledge bases
- **Authoring tools**: Writing Python tools, importing OpenAPI specs, or building agentic workflows
- **Managing connections**: Setting up authentication (Basic, Bearer, API Key, OAuth, SSO) for tools
- **Testing locally**: Using Developer Edition to test agents and tools before deployment
- **Deploying**: Moving agents from draft to live environments or deploying to production
- **Integrating**: Embedding agents in applications via web chat or APIs
- **Troubleshooting**: Debugging agent behavior, tool execution, or deployment issues

## Quick reference

### Essential CLI commands

| Task | Command |
|------|---------|
| Check ADK version | `orchestrate --version` |
| Get help | `orchestrate --help` or `orchestrate <command> --help` |
| List environments | `orchestrate env list` |
| Activate environment | `orchestrate env activate <env-name> --api-key <key>` |
| Import agent | `orchestrate agents import -f agent.yaml` |
| Create agent | `orchestrate agents create --name <name> --kind native --llm <model>` |
| Deploy agent | `orchestrate agents deploy --name <agent-name>` |
| Import Python tool | `orchestrate tools import -k python -f tool.py -r requirements.txt` |
| Import OpenAPI tool | `orchestrate tools import -k openapi -f spec.json` |
| Import agentic workflow | `orchestrate tools import -k flow -f flow.py` |
| List tools | `orchestrate tools list` |
| Add connection | `orchestrate connections add -a <app-id>` |
| Configure connection | `orchestrate connections configure -a <app-id> --env draft -t team -k basic` |
| Set credentials | `orchestrate connections set-credentials -a <app-id> --env draft -u <user> -p <pass>` |
| Import knowledge base | `orchestrate knowledge-bases import -f kb.yaml` |
| Chat with agent | `orchestrate chat ask "<prompt>"` |
| Run in debug mode | `orchestrate --debug <command>` |

### Agent configuration (YAML)

```yaml
spec_version: v1
kind: native
name: my_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default  # or react, react_intrinsic, planner
hide_reasoning: false
memory_enabled: false
description: "What this agent does"
instructions: |
  Your instructions to shape agent behavior
tools:
  - tool_name_1
  - tool_name_2
collaborators:
  - agent_name_1
knowledge_base:
  - kb_name
```

### Python tool structure

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool()
def my_tool(input_param: str) -> str:
    """Brief description of what the tool does.
    
    Args:
        input_param: Description of input
        
    Returns:
        str: Description of output
    """
    # Tool implementation
    return f"Result: {input_param}"
```

### Connection configuration (YAML)

```yaml
spec_version: v1
kind: connection
app_id: my_service
environments:
  draft:
    kind: basic  # or bearer, api_key, oauth_auth_code_flow, etc.
    type: team   # or member
    server_url: https://api.example.com/
  live:
    kind: basic
    type: team
    server_url: https://api.example.com/
```

### Agentic workflow structure

```python
from ibm_watsonx_orchestrate.agent_builder.flows import flow, Flow

@flow(
    name="my_workflow",
    display_name="My Workflow",
    input_schema=InputType,
    output_schema=OutputType
)
def build_my_workflow(aflow: Flow) -> Flow:
    node1 = aflow.tool(tool_function)
    node2 = aflow.tool(another_tool)
    
    aflow.sequence(START, node1, node2, END)
    return aflow
```

## Decision guidance

| Scenario | Use X | Use Y | When |
|----------|-------|-------|------|
| **Tool type** | Python tool | OpenAPI tool | Python for custom logic; OpenAPI for existing REST APIs |
| **Tool type** | Python tool | Agentic workflow | Python for simple functions; workflows for multi-step orchestration |
| **Agent style** | `default` | `react` | Default for simple tasks; React for complex reasoning |
| **Agent style** | `react` | `planner` | React for general use; Planner for explicit plan-then-act |
| **Connection scope** | `team` | `member` | Team for shared credentials; Member for per-user credentials |
| **Environment** | `local` | Remote (cloud/on-prem) | Local for development; Remote for production |
| **Deployment** | Draft only | Draft + Live | Draft for testing; Draft + Live for production |

## Workflow

### 1. Set up your environment
```bash
orchestrate env list                    # See available environments
orchestrate env activate local          # Use local Developer Edition
# OR
orchestrate env add -n prod -u <url>
orchestrate env activate prod --api-key <key>
```

### 2. Create or author your agent
- Write agent definition in `agents/my_agent.yaml` (or JSON/Python)
- Define instructions, tools, collaborators, knowledge base
- Validate syntax and structure

### 3. Create tools (if needed)
- **Python tool**: Write function with `@tool()` decorator in `tools/my_tool.py`
- **OpenAPI tool**: Provide OpenAPI spec file
- **Agentic workflow**: Define with `@flow()` decorator for multi-step orchestration
- Include `requirements.txt` for Python dependencies

### 4. Set up connections (if tools need authentication)
```bash
orchestrate connections add -a my_service
orchestrate connections configure -a my_service --env draft -t team -k basic
orchestrate connections set-credentials -a my_service --env draft -u user -p pass
```

### 5. Import tools into environment
```bash
orchestrate tools import -k python -f tools/my_tool.py -r requirements.txt
orchestrate tools import -k openapi -f tools/spec.json -a my_service
orchestrate tools import -k flow -f tools/my_flow.py
```

### 6. Import agent into environment
```bash
orchestrate agents import -f agents/my_agent.yaml
```

### 7. Test agent locally
```bash
orchestrate chat ask "What can you do?"
```

### 8. Deploy to production (if not Developer Edition)
```bash
orchestrate agents deploy --name my_agent
```

### 9. Verify deployment
```bash
orchestrate agents list
orchestrate tools list
orchestrate connections list
```

## Common gotchas

- **Environment timeout**: Remote environment authentication expires every 2 hours. Re-run `orchestrate env activate` if commands fail.
- **Missing requirements.txt**: Python tools fail to import if dependencies aren't declared. Always pin exact versions: `package==1.2.3`.
- **Connection not bound**: Tools won't work if connection is added but not configured or credentials not set. Check all three steps: add → configure → set-credentials.
- **Agent references non-existent tool**: Import tools before importing agents that use them. Agent import validates tool references.
- **Draft vs. Live confusion**: Developer Edition only has draft. Production has both. Deploy commands fail in Developer Edition.
- **Context variables not accessible**: Set `context_access_enabled: true` in agent YAML and list variables in `context_variables` to use them.
- **Tool timeout in workflows**: Agentic workflows run asynchronously and return instance IDs. Use "Get agentic workflow status" tool to check progress.
- **OAuth credentials not working**: Ensure OAuth connection is configured with correct token URL, client ID, and scopes. Test with `orchestrate connections list -v`.
- **File encoding issues**: If ADK fails to read files, set encoding: `orchestrate settings set-encoding utf-8`.
- **Python tool container networking**: In Developer Edition, localhost refers to container, not host. Use `docker.host.internal` or host IP to reach host services.

## Verification checklist

Before submitting work:

- [ ] Agent YAML/JSON is valid (check syntax with `orchestrate agents import --help`)
- [ ] All tools referenced in agent exist and are imported
- [ ] All connections used by tools are added, configured, and have credentials set
- [ ] Python tools have `@tool()` decorator and docstring
- [ ] Python tools have `requirements.txt` with pinned versions
- [ ] Agentic workflows have `@flow()` decorator and return Flow object
- [ ] Agent instructions are clear and guide LLM behavior
- [ ] Tool descriptions are accurate (LLM uses these to decide when to call)
- [ ] Knowledge base files are uploaded if agent uses `knowledge_base` field
- [ ] Test agent locally: `orchestrate chat ask "<test prompt>"`
- [ ] Verify no errors in output or logs
- [ ] For production: Deploy and verify with `orchestrate agents list`

## Resources

**Comprehensive navigation**: https://developer.watson-orchestrate.ibm.com/llms.txt

**Critical documentation pages**:
1. [Building native agents](https://developer.watson-orchestrate.ibm.com/agents/build_agent) — Agent configuration, styles, instructions, guidelines
2. [Authoring Python tools](https://developer.watson-orchestrate.ibm.com/tools/create_tool) — Tool decorators, dependencies, connections, schemas
3. [Agentic workflows](https://developer.watson-orchestrate.ibm.com/tools/flows/overview) — Multi-step orchestration, nodes, branching, loops

---

> For additional documentation and navigation, see: https://developer.watson-orchestrate.ibm.com/llms.txt
