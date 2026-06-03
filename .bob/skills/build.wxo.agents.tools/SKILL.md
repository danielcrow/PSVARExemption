---
name: build-wxo-agents-tools
description: Expert guidance for designing and implementing watsonx Orchestrate agents, flows, and tools with best practices and proven patterns
version: 1.0.0
tags:
  - watsonx-orchestrate
  - wxo
  - agent-development
  - flow-builder
  - tools
---

# Building watsonx Orchestrate Agents and Tools

## Overview

This skill provides comprehensive guidance for building watsonx Orchestrate (wxO) agents, flows, and tools. It covers core concepts, implementation patterns, and best practices based on the IBM watsonx Orchestrate Agent Development Kit (ADK).

**ADK Repository**: https://github.com/IBM/ibm-watsonx-orchestrate-adk

## Core Concepts

### 1. Agents
AI assistants that can use tools and interact with users. Agents are defined using YAML configuration files.

**Required Agent YAML Fields:**
```yaml
spec_version: v1                    # REQUIRED - Always use v1
kind: native                        # REQUIRED - Use 'native' for standard agents
name: agent_name                    # REQUIRED - Unique agent identifier
description: Agent description      # REQUIRED - Clear description of purpose
instructions: |                     # REQUIRED - Detailed instructions for LLM
  Step-by-step instructions for the agent
llm: groq/openai/gpt-oss-120b      # REQUIRED - LLM model to use
style: default                      # REQUIRED - Agent style (default, react, etc.)
collaborators: []                   # OPTIONAL - List of collaborator agents
tools:                              # REQUIRED - List of tools/flows
  - tool_or_flow_name
```

**CRITICAL**: Never omit `spec_version: v1` or other required fields - this will cause import errors.

### 2. Tools
Functions that agents can invoke. Three main types:

#### Python Tools
Python functions decorated with `@tool`:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.READ_ONLY)
def my_tool(param: str) -> dict:
    """Tool description that explains what it does"""
    # Implementation
    return {"result": "value"}
```

**Tool Permissions:**
- `ToolPermission.READ_ONLY` - For data retrieval, no modifications
- `ToolPermission.READ_WRITE` - For operations that modify data

#### Flow Tools
Workflows built with the flow builder (see Flow section below).

#### OpenAPI Tools
REST APIs defined by OpenAPI specifications.

### 3. Flows
Workflows that orchestrate multiple steps, tools, and logic.

**CRITICAL - Flow Function Signature:**
```python
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END

@flow(
    name="my_flow",
    display_name="My Flow",
    description="Flow description",
    input_schema=MyInputSchema
)
def build_my_flow(aflow: Flow) -> Flow:
    """
    MUST follow this exact signature:
    - Parameter MUST be named 'aflow' with type Flow
    - Function MUST return Flow
    - Function name MUST start with 'build_'
    """
    # Define flow nodes and sequence
    node1 = aflow.tool(my_tool_function)
    node2 = aflow.llm(
        prompt="Process this: {input}",
        system_prompt="You are a helpful assistant."  # REQUIRED
    )
    
    aflow.sequence(START, node1, node2, END)
    return aflow
```

**DO NOT:**
- ❌ Use alternative parameter names (e.g., `flow`, `f`, `builder`)
- ❌ Use different function signatures
- ❌ Omit the `build_` prefix from function name

### 4. Connections
Authenticated connections to external services.

**Credential Configuration:**
```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials
)

@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="gmail_connection",
            type=ConnectionType.OAUTH2_AUTH_CODE
        )
    ]
)
def send_email(to: str, subject: str, body: str, credentials: dict):
    """Send email using Gmail API"""
    access_token = credentials.get("access_token")
    # Use access_token for API calls
    return {"status": "sent"}
```

**Common ConnectionType Values:**
- `ConnectionType.OAUTH2_AUTH_CODE` - OAuth2 authorization code flow
- `ConnectionType.BASIC_AUTH` - Username/password authentication
- `ConnectionType.BEARER_TOKEN` - Bearer token authentication
- `ConnectionType.API_KEY_AUTH` - API key authentication

**CRITICAL:**
- Parameter name is `expected_credentials` (plural), not `expect_credentials`
- Use `ExpectedCredentials` objects, not plain dictionaries
- Import from `ibm_watsonx_orchestrate.agent_builder.connections`

## Standard Project Structure

```
project_name/
├── __init__.py                    # Python package initialization
├── README.md                      # Documentation with diagrams
├── main_flow.py                   # Programmatic testing (if flows exist)
├── import-all.sh                  # Import script for CLI
├── .env (optional)                # Environment variables
├── tools/                         # Tool implementations
│   ├── __init__.py
│   ├── tool_name.py              # Python tool definitions
│   └── flow_name.py              # Flow definitions
├── agents/                        # Agent configurations
│   └── agent_name.yaml           # Agent YAML files
└── generated/                     # Generated artifacts
    └── flow_spec.json            # Compiled flow specifications
```

## Implementation Patterns

### Pattern 1: Simple Python Tool

**Use Case**: Basic data retrieval or processing

```python
# tools/get_data.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.READ_ONLY)
def get_data(query: str) -> dict:
    """Retrieve data based on query"""
    # Implementation
    result = fetch_from_api(query)
    return {"data": result}
```

### Pattern 2: Tool with External Service Connection

**Use Case**: Integrate with external APIs requiring authentication

```python
# tools/external_service.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials
)

@tool(
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        ExpectedCredentials(
            app_id="service_connection",
            type=ConnectionType.OAUTH2_AUTH_CODE
        )
    ]
)
def call_external_service(param: str, credentials: dict) -> dict:
    """Call external service with OAuth2 authentication"""
    access_token = credentials.get("access_token")
    
    # Make API call with token
    response = requests.post(
        "https://api.service.com/endpoint",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"param": param}
    )
    
    return response.json()
```

### Pattern 3: Simple Flow with Tool

**Use Case**: Orchestrate tool execution with LLM processing

```python
# tools/processing_flow.py
from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
from .get_data import get_data

class FlowInput(BaseModel):
    query: str

class FlowOutput(BaseModel):
    summary: str

@flow(
    name="processing_flow",
    display_name="Data Processing Flow",
    description="Retrieve and summarize data",
    input_schema=FlowInput,
    output_schema=FlowOutput
)
def build_processing_flow(aflow: Flow) -> Flow:
    """Build flow that retrieves and processes data"""
    
    # Tool node to get data
    get_data_node = aflow.tool(get_data)
    
    # LLM node to summarize
    # IMPORTANT: system_prompt is REQUIRED
    summarize_node = aflow.prompt(
        name="summarize",
        system_prompt="You are a helpful assistant that summarizes data.",
        user_prompt=["Summarize this data: {data}"],
        output_schema=FlowOutput
    )
    
    # Map inputs
    get_data_node.map_input(
        input_variable="query",
        expression="flow.input.query"
    )
    
    summarize_node.map_input(
        input_variable="data",
        expression="flow['get_data'].output.data"
    )
    
    # Define sequence
    aflow.sequence(START, get_data_node, summarize_node, END)
    
    # Map output
    aflow.map_output(
        output_variable="summary",
        expression="flow['summarize'].output.summary"
    )
    
    return aflow
```

### Pattern 4: Document Processing Flow

**Use Case**: Extract structured data from documents (PDFs, images)

**CRITICAL - KVP Schema Definition:**
Always use `DocProcField` class for field definitions, not plain dictionaries.

```python
# tools/document_processing_flow.py
from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
from ibm_watsonx_orchestrate.flow_builder.types import (
    DocProcInput,
    DocProcKVPSchema,
    DocProcField,
    DocProcOutputFormat,
)

# Define KVP Schema using DocProcField
INVOICE_KVP_SCHEMA = DocProcKVPSchema(
    document_type="Invoice",
    document_description="Business invoice with itemized line items",
    additional_prompt_instructions="Extract all values exactly as they appear.",
    fields={
        "invoice_number": DocProcField(
            description="The unique identifier for the invoice",
            default="",
            example="INV-2024-001234",
        ),
        "invoice_date": DocProcField(
            description="The date the invoice was issued",
            default="",
            example="2024-01-15",
        ),
        "vendor_name": DocProcField(
            description="The name of the company issuing the invoice",
            default="",
            example="ABC Services Inc.",
        ),
        "total_amount": DocProcField(
            description="The final total amount due",
            default="",
            example="$6,464.25",
        ),
    }
)

class SummaryOutput(BaseModel):
    summary: str

@flow(
    name="invoice_processing",
    display_name="Invoice Processing Flow",
    description="Extract data from invoice documents",
    input_schema=DocProcInput
)
def build_invoice_processing(aflow: Flow) -> Flow:
    """Process invoice documents and extract structured data"""
    
    # Document processing node
    doc_node = aflow.docproc(
        name="extract_invoice_data",
        task="text_extraction",
        document_structure=True,
        enable_hw=True,
        output_format=DocProcOutputFormat.object,  # Returns JSON, not file
        kvp_schemas=[INVOICE_KVP_SCHEMA],
        kvp_force_schema_name="Invoice",
    )
    
    # Map document input
    doc_node.map_input(
        input_variable="document_ref",
        expression="flow.input.document_ref"
    )
    
    # Format KVPs with LLM (RECOMMENDED approach)
    # IMPORTANT: system_prompt is REQUIRED
    format_node = aflow.prompt(
        name="format_summary",
        system_prompt="You are a helpful assistant that formats invoice data.",
        user_prompt=["Format this invoice data in a user-friendly way: {kvps}"],
        output_schema=SummaryOutput
    )
    
    format_node.map_input(
        input_variable="kvps",
        expression="flow['extract_invoice_data'].output.kvps"
    )
    
    # Define sequence
    aflow.sequence(START, doc_node, format_node, END)
    
    # Map output
    aflow.map_output(
        output_variable="summary",
        expression="flow['format_summary'].output.summary"
    )
    
    return aflow
```

**CRITICAL - Document Processing KVP Structure:**

When using `output_format=DocProcOutputFormat.object`, the `kvps` field is a **list** of complex objects:

```json
{
  "key": {
    "semantic_label": "vendor_name",
    "raw_text": null
  },
  "value": {
    "raw_text": "ABC Store Inc.",
    "confidence_score": 0.95
  }
}
```

**Two Approaches to Handle KVPs:**

1. **Pass to Prompt Node** (Recommended)
   - Let LLM format the complex structure
   - More flexible and user-friendly

2. **Extract with List Comprehension**
   - Use single-line expressions in `map_output`
   - Match `semantic_label` and extract `raw_text`

```python
# Extract specific field value
aflow.map_output(
    output_variable="vendor_name",
    expression="[kvp['value']['raw_text'] for kvp in flow['extract_invoice_data'].output.kvps if kvp.get('key', {}).get('semantic_label') == 'vendor_name'][0] if [kvp for kvp in flow['extract_invoice_data'].output.kvps if kvp.get('key', {}).get('semantic_label') == 'vendor_name'] else ''"
)
```

**IMPORTANT - Document Upload Handling:**

When a flow expects a document as input (e.g., `DocProcInput`), the agent should invoke the flow tool directly. The flow itself handles the document upload prompt.

✅ **Correct Agent Instructions:**
```yaml
instructions: |
  When the user wants to process a document, immediately invoke the
  document_processing_flow tool. The flow will prompt for the document.
```

❌ **Incorrect:**
```yaml
instructions: |
  Ask the user to upload a document first, then pass it to the flow.
  # This will NOT work - agents cannot pass uploaded documents to flows
```

### Pattern 5: Conditional Flow

**Use Case**: Branch execution based on conditions

```python
# tools/conditional_flow.py
from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
from .check_condition import check_condition
from .handle_true import handle_true
from .handle_false import handle_false

class ConditionalInput(BaseModel):
    value: str

@flow(
    name="conditional_flow",
    display_name="Conditional Flow",
    description="Execute different paths based on condition",
    input_schema=ConditionalInput
)
def build_conditional_flow(aflow: Flow) -> Flow:
    """Flow with conditional branching"""
    
    check_node = aflow.tool(check_condition)
    true_branch = aflow.tool(handle_true)
    false_branch = aflow.tool(handle_false)
    
    # Map input to check node
    check_node.map_input(
        input_variable="value",
        expression="flow.input.value"
    )
    
    # Define sequence and branching
    aflow.sequence(START, check_node)
    aflow.if_else(
        condition="flow['check_condition'].output.is_valid",
        if_true=true_branch,
        if_false=false_branch
    )
    aflow.sequence(true_branch, END)
    aflow.sequence(false_branch, END)
    
    return aflow
```

### Pattern 6: User Activity Flow

**Use Case**: Interactive multi-step workflows with user input

```python
# tools/user_activity_flow.py
from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END

class ActivityInput(BaseModel):
    initial_data: str

@flow(
    name="user_activity_flow",
    display_name="User Activity Flow",
    description="Collect user input interactively",
    input_schema=ActivityInput
)
def build_user_activity_flow(aflow: Flow) -> Flow:
    """Flow with user activity nodes for input collection"""
    
    # User activity node for input collection
    activity_node = aflow.user_activity(
        name="collect_input",
        display_name="Collect User Input",
        description="Gather information from user"
    )
    
    # Process collected data
    process_node = aflow.tool(process_data)
    
    process_node.map_input(
        input_variable="user_data",
        expression="flow['collect_input'].output.data"
    )
    
    aflow.sequence(START, activity_node, process_node, END)
    
    return aflow
```

## CLI Commands Reference

### Import Commands

**CRITICAL**: Always use the `orchestrate` CLI commands to import components.

```bash
# Import Python tools
orchestrate tools import -k python -f tools/tool_name.py

# Import Flow tools
orchestrate tools import -k flow -f tools/flow_name.py

# Import agents
orchestrate agents import -f agents/agent_name.yaml

# Import connections
orchestrate connections import -f connections/connection_name.yaml
```

**DO NOT:**
- ❌ Use custom Python import scripts
- ❌ Use API client methods directly
- ❌ Invent alternative import methods

### List Commands

```bash
# List all agents
orchestrate agents list

# List all tools
orchestrate tools list

# List all connections
orchestrate connections list

# List environments
orchestrate env list
```

### Environment Commands

```bash
# Activate local environment
orchestrate env activate local

# Activate production environment
orchestrate env activate production

# Show current environment
orchestrate env show
```

### Chat Commands

```bash
# Start chat interface
orchestrate chat start

# Start chat with specific agent
orchestrate chat start --agent agent_name
```

### Debug Commands

```bash
# View recent traces
orchestrate observability traces search --last 1h

# Export specific trace
orchestrate observability traces export --trace-id <TRACE_ID>

# View logs
export LIMA_INSTANCE=ibm-watsonx-orchestrate
lima docker logs -f dev-edition-tools-runtime-1
lima docker logs dev-edition-wxo-tempus-runtime-1
```

## Import Script Template

**CRITICAL**: Use this exact format for `import-all.sh`:

```bash
#!/usr/bin/env bash

# Uncomment to activate local environment
# orchestrate env activate local

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Import Python tools
for tool in tool1.py tool2.py; do
  orchestrate tools import -k python -f ${SCRIPT_DIR}/tools/${tool}
done

# Import Flow tools
for flow in flow1.py flow2.py; do
  orchestrate tools import -k flow -f ${SCRIPT_DIR}/tools/${flow}
done

# Import connections (if any)
for conn in connection1.yaml; do
  orchestrate connections import -f ${SCRIPT_DIR}/connections/${conn}
done

# Import agents
for agent in agent1.yaml agent2.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done
```

Make executable: `chmod +x import-all.sh`

## Testing Approaches

### 1. Via Chat UI (Recommended for Agents)

```bash
cd project_directory
./import-all.sh
orchestrate chat start
# Select agent and interact
```

### 2. Programmatic Testing (For Flows)

```python
# main_flow.py
import asyncio
from pathlib import Path
from tools.my_flow import build_my_flow

async def main():
    # Compile and deploy flow
    flow_def = await build_my_flow().compile_deploy()
    
    # Save flow spec
    generated_folder = f"{Path(__file__).resolve().parent}/generated"
    flow_def.dump_spec(f"{generated_folder}/my_flow.json")
    
    # Test flow execution
    result = await flow_def.invoke(
        {"input_param": "test_value"},
        debug=True
    )
    
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run: `python3 main_flow.py`

## Best Practices

### 1. Agent Design
- ✅ Write clear, specific instructions
- ✅ Use appropriate LLM model for task complexity
- ✅ List only necessary tools (avoid tool overload)
- ✅ Test with various user inputs
- ❌ Don't make instructions too vague
- ❌ Don't give agents too many tools

### 2. Tool Design
- ✅ Keep tools focused and single-purpose
- ✅ Use descriptive names and docstrings
- ✅ Include proper type hints
- ✅ Handle errors gracefully
- ✅ Use appropriate permissions (READ_ONLY vs READ_WRITE)
- ❌ Don't create overly complex tools
- ❌ Don't mix multiple concerns in one tool

### 3. Flow Design
- ✅ Use correct function signature: `def build_<name>(aflow: Flow) -> Flow:`
- ✅ Map inputs and outputs explicitly
- ✅ Include system_prompt in all prompt nodes
- ✅ Use Pydantic models for schemas
- ✅ Test flows programmatically before agent integration
- ❌ Don't use dynamic type creation for Pydantic models
- ❌ Don't define Python functions in expressions
- ❌ Don't omit required parameters

### 4. Connection Management
- ✅ Use `expected_credentials` parameter correctly
- ✅ Import `ExpectedCredentials` and `ConnectionType`
- ✅ Store credentials securely
- ✅ Test authentication before deployment
- ❌ Don't hardcode credentials in code
- ❌ Don't use plain dictionaries for credentials

### 5. Documentation
- ✅ Include README with architecture and workflow diagrams
- ✅ Document all inputs, outputs, and dependencies
- ✅ Provide usage examples
- ✅ Keep documentation updated
- ❌ Don't skip diagram creation
- ❌ Don't leave undocumented components

### 6. Error Handling
- ✅ Use try-except blocks for external calls
- ✅ Provide meaningful error messages
- ✅ Log errors for debugging
- ✅ Handle edge cases gracefully
- ❌ Don't let exceptions crash tools
- ❌ Don't return generic error messages

### 7. Type Safety
- ✅ Define Pydantic models as proper classes
- ✅ Use type hints in function signatures
- ✅ Validate inputs with Pydantic
- ❌ Don't use dynamic type creation
- ❌ Don't skip type annotations

## Common Pitfalls and Solutions

### Pitfall 1: Missing spec_version in Agent YAML
**Error**: Import fails with "spec_version missing"
**Solution**: Always include `spec_version: v1` in agent YAML

### Pitfall 2: Wrong Flow Function Signature
**Error**: Flow function signature error
**Solution**: Use exact signature: `def build_<name>(aflow: Flow) -> Flow:`

### Pitfall 3: Wrong Credential Parameter Name
**Error**: `expect_credentials` not recognized
**Solution**: Use `expected_credentials` (plural)

### Pitfall 4: Dynamic Pydantic Model Creation
**Error**: "non-annotated attribute" errors
**Solution**: Define models as proper classes, not dynamic types

### Pitfall 5: Missing system_prompt in Prompt Nodes
**Error**: Prompt node fails validation
**Solution**: Always include `system_prompt` parameter

### Pitfall 6: Complex Expressions in map_output
**Error**: Expression evaluation fails
**Solution**: Use single-line expressions only, no function definitions

### Pitfall 7: Wrong Document Upload Handling
**Error**: Agent asks for document but can't pass it to flow
**Solution**: Let flow handle document upload, agent just invokes flow

### Pitfall 8: Wrong KVP Access Pattern
**Error**: Cannot access KVP values
**Solution**: Use `kvp['key']['semantic_label']` and `kvp['value']['raw_text']`

## Quick Start Checklist

When creating a new watsonx Orchestrate project:

- [ ] Create project directory structure
- [ ] Define Pydantic input/output schemas
- [ ] Implement Python tools (if needed)
- [ ] Create flows with correct function signatures
- [ ] Define agent YAML with all required fields
- [ ] Create import-all.sh script
- [ ] Create main_flow.py for testing (if flows exist)
- [ ] Write README with architecture and workflow diagrams
- [ ] Test locally with chat UI
- [ ] Test flows programmatically
- [ ] Document all components
- [ ] Create connection YAMLs (if external services used)
- [ ] Set up environment variables
- [ ] Verify all imports work
- [ ] Test end-to-end scenarios

## Resources

- **Official Documentation**: https://developer.watson-orchestrate.ibm.com
- **ADK GitHub**: https://github.com/IBM/watsonx-orchestrate-adk
- **Examples**: https://github.com/IBM/watsonx-orchestrate-adk/tree/main/examples
- **Code Blocks Documentation**: https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=workflows-code-blocks