---
name: build-wxo-sop
description: Expert guidance for creating Standard Operating Procedures (SOPs) for watsonx Orchestrate projects including agents, flows, tools, and deployment processes
version: 1.0.0
tags:
  - watsonx-orchestrate
  - wxo
  - sop
  - documentation
  - best-practices
---

# Building SOPs for watsonx Orchestrate Projects

## Overview

This skill provides guidance for creating comprehensive Standard Operating Procedures (SOPs) for watsonx Orchestrate (wxO) projects. SOPs ensure consistency, maintainability, and knowledge transfer across teams.

## SOP Structure Template

### 1. Project Overview Section
```markdown
# [Project Name] - watsonx Orchestrate Implementation

## Purpose
Brief description of what the project accomplishes and business value.

## Scope
- What is included in this implementation
- What is excluded
- Dependencies and prerequisites

## Architecture Overview
High-level diagram showing:
- Agents and their roles
- Flows and their purposes
- Tools and integrations
- External services/APIs
- Knowledge bases (if applicable)
```

### 2. Environment Setup Section
```markdown
## Environment Setup

### Prerequisites
- Python 3.11+
- watsonx Orchestrate ADK installed
- Required API keys and credentials
- Access to watsonx Orchestrate instance

### Installation Steps
1. Clone repository: `git clone [repo-url]`
2. Create virtual environment: `python3 -m venv venv`
3. Activate environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure environment variables (see .env.example)

### Environment Variables
List all required environment variables:
- `WXO_API_KEY`: watsonx Orchestrate API key
- `SERVICE_API_KEY`: External service credentials
- etc.
```

### 3. Project Structure Section
```markdown
## Project Structure

```
project_name/
├── agents/                    # Agent YAML configurations
│   ├── main_agent.yaml
│   └── specialist_agent.yaml
├── tools/                     # Tool implementations
│   ├── __init__.py
│   ├── python_tool.py        # Python tools
│   └── flow_tool.py          # Flow definitions
├── connections/               # Connection configurations
│   └── service_connection.yaml
├── knowledge-bases/          # Knowledge base documents
├── generated/                # Generated flow specs
├── tests/                    # Test files
├── import-all.sh            # Import script
├── main_flow.py             # Programmatic testing
├── .env.example             # Environment template
└── README.md                # Project documentation
```
```

### 4. Component Documentation Section
```markdown
## Components

### Agents

#### [Agent Name]
- **Purpose**: What this agent does
- **Configuration**: `agents/agent_name.yaml`
- **Tools Used**: List of tools this agent can invoke
- **LLM Model**: Model used (e.g., groq/openai/gpt-oss-120b)
- **Instructions**: Key instructions given to the agent

### Flows

#### [Flow Name]
- **Purpose**: What this flow accomplishes
- **Input Schema**: Expected input parameters
- **Output Schema**: What the flow returns
- **Workflow Diagram**: Mermaid diagram showing flow steps
- **Key Nodes**:
  - Node 1: Description
  - Node 2: Description

### Tools

#### [Tool Name]
- **Type**: Python tool / Flow tool / OpenAPI tool
- **Purpose**: What this tool does
- **Parameters**: Input parameters and types
- **Returns**: Output format
- **Permissions**: READ_ONLY / READ_WRITE
- **Dependencies**: External services or APIs used

### Connections

#### [Connection Name]
- **Type**: OAuth2 / Basic Auth / API Key / Bearer Token
- **Service**: External service name
- **Configuration**: `connections/connection_name.yaml`
- **Required Credentials**: List of required fields
- **Setup Instructions**: How to obtain and configure credentials
```

### 5. Deployment Procedures Section
```markdown
## Deployment Procedures

### Local Development Environment

1. **Activate Environment**
   ```bash
   source venv/bin/activate
   ```

2. **Import Components**
   ```bash
   ./import-all.sh
   ```

3. **Test Agents**
   ```bash
   orchestrate chat start
   # Select agent and test interactions
   ```

4. **Programmatic Testing** (for flows)
   ```bash
   export PYTHONPATH=/path/to/adk/src:/path/to/adk
   python3 main_flow.py
   ```

### Production Deployment

1. **Pre-deployment Checklist**
   - [ ] All tests passing
   - [ ] Environment variables configured
   - [ ] Credentials validated
   - [ ] Documentation updated
   - [ ] Change approval obtained

2. **Deployment Steps**
   ```bash
   # Switch to production environment
   orchestrate env activate production
   
   # Import components
   ./import-all.sh
   
   # Verify deployment
   orchestrate agents list
   orchestrate tools list
   ```

3. **Post-deployment Verification**
   - Test agent interactions
   - Verify tool executions
   - Check connection status
   - Monitor logs for errors

### Rollback Procedures

If deployment fails:
1. Switch to previous environment
2. Re-import previous version
3. Verify functionality
4. Document issues encountered
```

### 6. Testing Procedures Section
```markdown
## Testing Procedures

### Unit Testing

Test individual tools:
```python
# Test Python tool
from tools.my_tool import my_tool

result = my_tool(param="test_value")
assert result["status"] == "success"
```

### Integration Testing

Test flows programmatically:
```python
# Test flow execution
import asyncio
from tools.my_flow import build_my_flow

async def test_flow():
    flow_def = await build_my_flow().compile_deploy()
    result = await flow_def.invoke({"input": "test"}, debug=True)
    assert result["output"] is not None

asyncio.run(test_flow())
```

### End-to-End Testing

1. Launch chat interface: `orchestrate chat start`
2. Select agent
3. Test scenarios:
   - Happy path: Expected inputs and outputs
   - Edge cases: Boundary conditions
   - Error handling: Invalid inputs
4. Document results

### Test Cases

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| TC-001 | Valid input | Success response | ✅ |
| TC-002 | Invalid input | Error message | ✅ |
| TC-003 | Edge case | Handled gracefully | ✅ |
```

### 7. Troubleshooting Section
```markdown
## Troubleshooting

### Common Issues

#### Issue: Import fails with "spec_version missing"
**Cause**: Agent YAML missing required `spec_version: v1` field
**Solution**: Add `spec_version: v1` to agent YAML file

#### Issue: Flow function signature error
**Cause**: Flow function doesn't match required signature
**Solution**: Ensure function signature is `def build_<flow_name>(aflow: Flow) -> Flow:`

#### Issue: Tool not found by agent
**Cause**: Tool not imported or name mismatch
**Solution**: 
1. Verify tool imported: `orchestrate tools list`
2. Check tool name matches agent YAML
3. Re-import: `orchestrate tools import -k python -f tools/tool_name.py`

#### Issue: Connection authentication fails
**Cause**: Invalid credentials or expired tokens
**Solution**:
1. Verify credentials in connection YAML
2. Re-authenticate if using OAuth2
3. Check API key validity

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

# List components
orchestrate agents list
orchestrate tools list
orchestrate connections list
```

### Getting Help

- Documentation: https://developer.watson-orchestrate.ibm.com
- GitHub: https://github.com/IBM/watsonx-orchestrate-adk
- Support: IBM watsonx Orchestrate support channels
```

### 8. Maintenance Section
```markdown
## Maintenance

### Regular Maintenance Tasks

#### Weekly
- Review agent performance metrics
- Check for failed tool executions
- Monitor API rate limits
- Review error logs

#### Monthly
- Update dependencies
- Review and update documentation
- Audit credentials and rotate if needed
- Performance optimization review

#### Quarterly
- Security audit
- Disaster recovery testing
- Knowledge base updates
- User feedback review

### Version Control

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Tag releases in Git
- Maintain CHANGELOG.md
- Document breaking changes

### Backup Procedures

1. Export agent configurations
2. Backup connection credentials (securely)
3. Archive flow specifications
4. Document custom tools
5. Store in version control and secure backup location
```

## SOP Creation Checklist

When creating an SOP for a watsonx Orchestrate project, ensure you include:

- [ ] Project overview and purpose
- [ ] Architecture diagrams (system and workflow)
- [ ] Environment setup instructions
- [ ] Project structure documentation
- [ ] Component documentation (agents, flows, tools, connections)
- [ ] Deployment procedures (local and production)
- [ ] Testing procedures and test cases
- [ ] Troubleshooting guide
- [ ] Maintenance schedule and procedures
- [ ] Version control strategy
- [ ] Contact information and escalation paths

## Best Practices

1. **Keep SOPs Updated**: Review and update after each significant change
2. **Use Visual Aids**: Include Mermaid diagrams for architecture and workflows
3. **Be Specific**: Provide exact commands and file paths
4. **Include Examples**: Show real examples from the project
5. **Test Instructions**: Verify all procedures work as documented
6. **Version SOPs**: Track SOP versions alongside code versions
7. **Make Accessible**: Store in easily accessible location (wiki, repo, etc.)
8. **Get Feedback**: Have team members review and validate SOPs
9. **Include Rationale**: Explain why certain approaches are used
10. **Link Resources**: Reference official documentation and related materials

## SOP Templates by Project Type

### Simple Agent with Tools
Focus on: Agent configuration, tool documentation, basic testing

### Document Processing Flow
Focus on: KVP schema definition, document upload handling, extraction validation

### Multi-Agent Collaboration
Focus on: Agent roles, collaboration patterns, coordination flows

### Integration-Heavy Project
Focus on: Connection setup, API documentation, error handling

### Production-Scale Deployment
Focus on: Deployment automation, monitoring, incident response