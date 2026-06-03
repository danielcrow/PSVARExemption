# PSVAR Exemption Agents

This directory contains the watsonx Orchestrate agents for the PSVAR exemption assessment workflow.

## Agents

### 1. PSVAR Intake Agent (`psvar_intake_agent.yaml`)

**Purpose**: Primary interface for transport operators applying for PSVAR exemptions

**LLM Model**: `groq/openai/gpt-oss-120b`

**Type**: Native agent

**Responsibilities**:
- Greet operators and explain the assessment process
- Invoke the assessment flow to collect information and evaluate eligibility
- Present results in user-friendly language
- Send email notifications with outcomes
- Handle follow-up questions

**Tools**:
- `psvar_exemption_assessment_flow` - Main assessment flow
- `send_assessment_outcome_email` - Email notification tool

**Usage**:
```bash
# Import the agent
orchestrate agents import -f agents/psvar_intake_agent.yaml

# Start chat with the agent
orchestrate chat start
# Select: psvar_intake_agent
```

**Key Features**:
- Conversational interface for data collection
- Automatic assessment evaluation
- Email notifications with evidence transcripts
- Clear explanation of outcomes and next steps

---

### 2. PSVAR Exemption Assessor (`psvar_exemption_assessor.yaml`)

**Purpose**: Detailed assessment agent with comprehensive interview process

**LLM Model**: `groq/openai/gpt-oss-120b`

**Type**: Native agent

**Responsibilities**:
- Conduct detailed interviews with operators
- Collect all required information systematically
- Validate VINs and fleet data
- Evaluate compliance against progressive milestones
- Generate assessment outcomes with rationale

**Tools**:
- `psvar_exemption_assessment_flow` - Main assessment flow
- `send_assessment_outcome_email` - Email notification tool

**Usage**:
```bash
# Import the agent
orchestrate agents import -f agents/psvar_exemption_assessor.yaml

# Start chat with the agent
orchestrate chat start
# Select: psvar_exemption_assessment
```

**Key Features**:
- Form-like data collection experience
- VIN validation during conversation
- Dynamic questioning based on previous answers
- Comprehensive instructions for handling edge cases
- Evidence transcript generation

---

### 3. PSVAR Exemption Form Agent (`psvar_exemption_form_agent.yaml`)

**Purpose**: Interactive form-based assessment agent

**LLM Model**: `groq/openai/gpt-oss-120b`

**Type**: Native agent

**Responsibilities**:
- Collect information through conversational forms
- Use conditional logic to skip unnecessary questions
- Evaluate exemption eligibility
- Present results with clear rationale

**Tools**:
- `psvar_exemption_form_tool` - Form-based data collection
- `psvar_exemption_assessment_flow` - Assessment evaluation

**Usage**:
```bash
# Import the agent
orchestrate agents import -f agents/psvar_exemption_form_agent.yaml

# Start chat with the agent
orchestrate chat start
# Select: psvar_exemption_form_agent
```

**Key Features**:
- Conditional question flow
- Skips irrelevant questions based on responses
- Clear section-based organization
- User-friendly result presentation

---

## Deployment

To deploy all agents:

```bash
# Run the import script from the project root
./import-all.sh
```

This will import:
1. All Python tools
2. All flow tools
3. All agents (including psvar_intake_agent)

## Agent Selection Guide

**Use `psvar_intake_agent` when**:
- You want a streamlined, simple interface
- The operator needs quick guidance through the process
- You want the most user-friendly experience

**Use `psvar_exemption_assessor` when**:
- You need detailed, comprehensive assessment
- The case may be complex or edge-case scenarios
- You want maximum control over the interview process

**Use `psvar_exemption_form_agent` when**:
- You prefer a structured form-based approach
- You want conditional logic to skip irrelevant questions
- You need a balance between simplicity and detail

## Configuration

All agents use:
- **LLM**: `groq/openai/gpt-oss-120b`
- **Style**: `default`
- **Kind**: `native`

## Related Documentation

- [Implementation Plan](../WATSONX_ORCHESTRATE_IMPLEMENTATION_PLAN.md)
- [Workflow Requirements](../PSVAR_WORKFLOW_AND_DATA_REQUIREMENTS.md)
- [Workflow Diagrams](../PSVAR_WORKFLOW_DIAGRAMS.md)