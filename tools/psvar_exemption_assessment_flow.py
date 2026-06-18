from ibm_watsonx_orchestrate.flow_builder.flows import END, START, Flow, flow

from .evaluate_psvar_exemption import (
    PSVARAssessmentInput,
    PSVARAssessmentOutput,
    evaluate_psvar_exemption,
)
from .generate_exemption_certificate import (
    CertificateData,
    VehicleEntry,
    generate_exemption_certificate,
)


@flow(
    name="psvar_exemption_assessment_flow",
    display_name="PSVAR Exemption Assessment Flow",
    description="Collects structured operator answers and evaluates whether the operator can rely on the PSVAR exemption guidance.",
    input_schema=PSVARAssessmentInput,
    output_schema=PSVARAssessmentOutput,
)
def build_psvar_exemption_assessment_flow(aflow: Flow) -> Flow:
    """
    Build the PSVAR exemption assessment flow.

    This flow accepts structured assessment input and invokes the
    deterministic rules tool to produce a decision. Certificate generation
    is handled within the evaluation tool based on the outcome.
    """
    assessment_node = aflow.tool(evaluate_psvar_exemption)
    
    # Simple linear flow - certificate generation is conditional within the tool
    aflow.sequence(START, assessment_node, END)

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
