# PSVAR Exemption Form Agent Guide

## Overview

The **PSVAR Exemption Form Agent** (`psvar_exemption_form_agent`) provides an interactive, conversational way to collect operator information and assess PSVAR exemption eligibility. Unlike the direct tool invocation approach, this agent guides users through the assessment process step-by-step.

## Features

- **Conversational Interface**: Friendly, guided conversation that collects information naturally
- **Structured Data Collection**: Systematically gathers all required information across 7 sections
- **Intelligent Validation**: Asks clarifying questions when information is unclear
- **Clear Results**: Presents assessment outcomes with rationale and next actions
- **Flexible Input**: Accepts various formats for boolean responses and service types

## How It Works

### 1. Information Collection Process

The agent collects information in a structured order:

#### Section 1: Operator Information
- Company name (required)
- Operator licence number
- Contact details (name, phone, email)
- Postal address and postcode

#### Section 2: Service Information
- Service types (HTS = Home-to-School, RR = Rail Replacement)
- For HTS services:
  - Whether services are closed-door
  - Whether there are paying customers

#### Section 3: Fleet Information
- Total HTS fleet size (required)
- Number of fully compliant vehicles
- Number of partially compliant vehicles
- Number of non-compliant vehicles
- Vehicles temporarily out of service

#### Section 4: Vehicle Identification Numbers
- VINs for all vehicles (17 characters each)
- VINs for partially compliant vehicles
- VINs for non-compliant vehicles

#### Section 5: Exemption Certificate
- Whether an exemption certificate exists (required)
- If yes:
  - Start date (YYYY-MM-DD)
  - End date (YYYY-MM-DD)
  - Certificate reference number

#### Section 6: Operational Conditions (if exemption exists)
- Exemption copy carried onboard
- Alternative accessible transport availability
- Written confirmation retention
- Band compliance requirements acknowledgment

#### Section 7: Fleet Changes (if exemption exists)
- Whether fleet size has changed since exemption grant
- Whether DfT was notified within 5 working days

### 2. Assessment Evaluation

Once sufficient information is collected:
1. Agent summarizes collected data
2. Asks for confirmation or corrections
3. Invokes the `psvar_exemption_assessment_flow` tool
4. Evaluates eligibility using deterministic rules

### 3. Results Presentation

The agent presents:
- **Decision Outcome**: Overall assessment result
- **Scope Status**: Whether service is in scope
- **Exemption Status**: Whether exemption is needed/valid
- **Compliance Band**: A, B, C, or D (if applicable)
- **Rationale**: Detailed reasons for the decision
- **Next Actions**: Recommended steps
- **Missing Information**: What additional data would improve assessment

## Usage

### Via Chat UI

1. **Import the agent**:
   ```bash
   ./import-all.sh
   ```

2. **Start chat**:
   ```bash
   orchestrate chat start
   ```

3. **Select the agent**:
   - Choose `psvar_exemption_form_agent` from the agent list

4. **Begin conversation**:
   - The agent will greet you and begin collecting information
   - Answer questions naturally
   - The agent will guide you through all required sections

### Example Conversation Flow

```
Agent: Hello! I'm here to help assess your PSVAR exemption eligibility for 
       home-to-school transport services. I'll need to collect some information 
       from you. Let's start with your company details.
       
       What is your company name?

User: ABC Transport Ltd

Agent: Thank you. Do you have an operator licence number?

User: Yes, it's OL123456

Agent: Great. Now, let's talk about your services. What types of services 
       do you operate? (HTS for home-to-school, RR for rail replacement)

User: We operate home-to-school services

Agent: Perfect. Are these home-to-school services closed-door services? 
       That means they're pre-booked and not available to the general public.

User: Yes, they are closed-door

[... conversation continues through all sections ...]

Agent: Thank you for providing all that information. Let me summarize what 
       I've collected:
       - Company: ABC Transport Ltd
       - Licence: OL123456
       - Service: HTS (closed-door, paying customers)
       - Fleet: 10 vehicles (3 fully compliant, 5 partially, 2 non-compliant)
       - Exemption: Yes, valid until 2026-07-31
       
       Is this correct, or would you like to make any changes?

User: That's correct

Agent: Excellent. Let me assess your exemption eligibility now...
       
       [Assessment results presented with decision, rationale, and next actions]
```

## Assessment Outcomes

### CAN_HAVE_EXEMPTION
- Operator meets all requirements
- Valid exemption certificate exists
- Compliant with operational conditions
- **Next Actions**: Continue monitoring compliance

### CANNOT_HAVE_EXEMPTION
- Operator fails to meet requirements
- May have expired certificate or non-compliance
- **Next Actions**: Address identified issues

### FURTHER_INVESTIGATION_REQUIRED
- Missing critical information
- Potential compliance issues need verification
- **Next Actions**: Provide missing information or DVSA review

### OUT_OF_SCOPE
- Service doesn't require PSVAR exemption
- Examples: No paying customers, not HTS/RR service
- **Next Actions**: No exemption needed

### EXEMPTION_NOT_REQUIRED
- All vehicles are fully PSVAR compliant
- No exemption necessary
- **Next Actions**: Maintain full compliance

## Advantages Over Direct Tool Invocation

1. **User-Friendly**: No need to understand complex data structures
2. **Guided Process**: Agent asks relevant follow-up questions
3. **Flexible Input**: Accepts natural language responses
4. **Error Prevention**: Validates data as it's collected
5. **Clear Communication**: Explains requirements and results in plain language

## Technical Details

### Agent Configuration
- **Name**: `psvar_exemption_form_agent`
- **LLM**: `groq/openai/gpt-oss-120b`
- **Style**: `default`
- **Tools**: `psvar_exemption_assessment_flow`

### Data Flow
```
User Input → Agent Conversation → Data Collection → 
PSVARAssessmentInput → evaluate_psvar_exemption Tool → 
PSVARAssessmentOutput → Agent Presentation → User
```

## Comparison with Other Agents

| Feature | Form Agent | Direct Assessor Agent |
|---------|-----------|----------------------|
| Data Collection | Conversational | Requires structured input |
| User Experience | Guided, step-by-step | Expects all data upfront |
| Flexibility | High (natural language) | Low (strict schema) |
| Error Handling | Interactive clarification | Validation errors |
| Best For | End users, operators | API integration, automation |

## Tips for Best Results

1. **Be Specific**: Provide exact numbers and dates when asked
2. **VIN Format**: Ensure VINs are exactly 17 characters
3. **Date Format**: Use YYYY-MM-DD format for dates
4. **Boolean Questions**: Answer yes/no, true/false, or similar
5. **Service Types**: Use "HTS" or "home-to-school" for clarity
6. **Review Summary**: Check the agent's summary before final assessment

## Troubleshooting

### Agent doesn't understand my response
- Try rephrasing in simpler terms
- Use explicit yes/no for boolean questions
- Provide numbers without units (e.g., "5" not "5 vehicles")

### Missing information in results
- The agent will list what's missing
- Provide the additional information
- Agent can re-run assessment with updated data

### Incorrect assessment
- Review the rationale provided
- Check if all information was collected correctly
- Provide corrections and ask for re-assessment

## Related Files

- **Agent Configuration**: `agents/psvar_exemption_form_agent.yaml`
- **Flow Tool**: `tools/psvar_exemption_assessment_flow.py`
- **Evaluation Logic**: `tools/evaluate_psvar_exemption.py`
- **Import Script**: `import-all.sh`

## Support

For issues or questions:
1. Check the rationale and missing information in assessment results
2. Review the PSVAR exemption guidance documentation
3. Contact DVSA for regulatory clarification

---

**Made with Bob**