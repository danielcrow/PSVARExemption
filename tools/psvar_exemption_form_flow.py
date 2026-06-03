from datetime import date
from typing import Optional

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import END, START, Flow, flow

from .evaluate_psvar_exemption import (
    PSVARAssessmentInput,
    PSVARAssessmentOutput,
    evaluate_psvar_exemption,
)


class PSVARFormFlowInput(BaseModel):
    """Empty input schema - user activity collects all data."""
    pass


@flow(
    name="psvar_exemption_form_flow",
    display_name="PSVAR Exemption Assessment Form",
    description="Interactive form to collect operator information and assess PSVAR exemption eligibility.",
    input_schema=PSVARFormFlowInput,
    output_schema=PSVARAssessmentOutput,
)
def build_psvar_exemption_form_flow(aflow: Flow) -> Flow:
    """
    Build the PSVAR exemption assessment flow with an interactive user activity form.
    
    This flow presents a user activity to collect all required information,
    then evaluates the exemption eligibility using the deterministic rules.
    """
    
    # Create user activity node to collect assessment data
    # The user_activity node will present a form to the user in the chat UI
    collect_data_node = aflow.user_activity(
        name="collect_assessment_data",
        display_name="PSVAR Exemption Assessment Form",
        description="""Please provide the following information to assess your PSVAR exemption eligibility.

**Section 1: Operator Information**
- Company Name (required)
- Operator Licence Number
- Authorised Contact Name
- Contact Telephone
- Contact Email
- Postal Address
- Postcode

**Section 2: Service Information**
- Service Types (HTS = Home-to-School, RR = Rail Replacement)
- Are HTS services closed-door? (yes/no)
- Do HTS services have paying customers? (yes/no)

**Section 3: Fleet Information**
- Total HTS Fleet Size (required)
- Number of Fully Compliant Vehicles (required)
- Number of Partially Compliant Vehicles (required)
- Number of Non-Compliant Vehicles (required)
- Number of Vehicles Temporarily Out of Service

**Section 4: Vehicle Identification Numbers**
- VINs for all vehicles (comma-separated, 17 characters each)
- VINs for partially compliant vehicles (comma-separated)
- VINs for non-compliant vehicles (comma-separated)

**Section 5: Exemption Certificate**
- Do you hold an exemption certificate? (yes/no, required)
- Exemption Start Date (YYYY-MM-DD)
- Exemption End Date (YYYY-MM-DD)
- Exemption Certificate Reference

**Section 6: Operational Conditions** (if you have an exemption)
- Is exemption copy carried onboard? (yes/no)
- Is alternative accessible transport available? (yes/no)
- Is written confirmation retained? (yes/no)
- Have you read band compliance requirements? (yes/no)

**Section 7: Fleet Changes** (if you have an exemption)
- Has fleet size changed since exemption grant? (yes/no)
- If yes, was DfT notified within 5 working days? (yes/no)

Please provide as much information as possible for an accurate assessment.""",
        input_schema=PSVARAssessmentInput,
    )
    
    # Evaluate the assessment using the tool
    # The user_activity node output will match PSVARAssessmentInput schema
    assessment_node = aflow.tool(evaluate_psvar_exemption)
    
    # Map the user activity output directly to the assessment tool
    assessment_node.map_input(
        input_variable="assessment",
        expression="flow['collect_assessment_data'].output"
    )
    
    # Sequence the nodes
    aflow.sequence(START, collect_data_node, assessment_node, END)
    
    # Map all outputs from the assessment
    aflow.map_output(
        output_variable="decision",
        expression="flow['evaluate_psvar_exemption'].output.decision"
    )
    aflow.map_output(
        output_variable="final_case_outcome",
        expression="flow['evaluate_psvar_exemption'].output.final_case_outcome"
    )
    aflow.map_output(
        output_variable="in_scope",
        expression="flow['evaluate_psvar_exemption'].output.in_scope"
    )
    aflow.map_output(
        output_variable="exemption_needed",
        expression="flow['evaluate_psvar_exemption'].output.exemption_needed"
    )
    aflow.map_output(
        output_variable="valid_exemption_certificate",
        expression="flow['evaluate_psvar_exemption'].output.valid_exemption_certificate"
    )
    aflow.map_output(
        output_variable="compliance_band",
        expression="flow['evaluate_psvar_exemption'].output.compliance_band"
    )
    aflow.map_output(
        output_variable="milestone_compliant",
        expression="flow['evaluate_psvar_exemption'].output.milestone_compliant"
    )
    aflow.map_output(
        output_variable="operational_conditions_compliant",
        expression="flow['evaluate_psvar_exemption'].output.operational_conditions_compliant"
    )
    aflow.map_output(
        output_variable="dvsa_task_payload",
        expression="flow['evaluate_psvar_exemption'].output.dvsa_task_payload"
    )
    aflow.map_output(
        output_variable="email_notification_payload",
        expression="flow['evaluate_psvar_exemption'].output.email_notification_payload"
    )
    aflow.map_output(
        output_variable="rationale",
        expression="flow['evaluate_psvar_exemption'].output.rationale"
    )
    aflow.map_output(
        output_variable="next_actions",
        expression="flow['evaluate_psvar_exemption'].output.next_actions"
    )
    aflow.map_output(
        output_variable="missing_information",
        expression="flow['evaluate_psvar_exemption'].output.missing_information"
    )
    
    return aflow


# Made with Bob