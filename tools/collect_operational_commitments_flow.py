"""
Flow to collect operational commitments for PSVAR exemption assessment.
This is Section 5 of the data collection process - presented as a form.
Only needed if partially/non-compliant vehicles exist.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END


class OperationalCommitmentsInput(BaseModel):
    """Input to start the operational commitments collection flow"""
    pass


class OperationalCommitmentsOutput(BaseModel):
    """Output from operational commitments collection"""
    will_carry_certificate_onboard: bool = Field(
        description="Will carry exemption certificate onboard partially/non-compliant vehicles"
    )
    alternative_transport_available: bool = Field(
        description="Alternative accessible transport will be available when needed"
    )
    written_confirmation_retained: bool = Field(
        description="Will retain written confirmation of alternative transport arrangements"
    )
    all_commitments_met: bool = Field(description="Whether all required commitments are met")
    missing_commitments: list[str] = Field(description="List of missing commitments", default_factory=list)
    message: str = Field(description="Confirmation message")


@flow(
    name="collect_operational_commitments",
    display_name="Section 5: Operational Commitments",
    description="Collect operational commitments via form",
    input_schema=OperationalCommitmentsInput,
    output_schema=OperationalCommitmentsOutput
)
def build_collect_operational_commitments(aflow: Flow) -> Flow:
    """
    CRITICAL: Flow function signature MUST be:
    def build_<flow_name>(aflow: Flow) -> Flow:
    """
    
    # Create user flow for form
    user_flow = aflow.userflow()
    user_flow.spec.display_name = "Operational Commitments"
    
    # Create form
    commitments_form = user_flow.form(
        name="operational_commitments_form",
        display_name="Operational Commitments",
        instructions="The following commitments are REQUIRED for exemption eligibility when using partially compliant or non-compliant vehicles. All three commitments must be confirmed.",
        submit_button_label="Complete Data Collection",
        cancel_button_label=None  # Hide cancel button
    )
    
    # Add form fields - all as checkboxes that must be checked
    commitments_form.boolean_input_field(
        name="will_carry_certificate_onboard",
        label="I will carry a copy of the exemption certificate onboard each partially/non-compliant vehicle",
        single_checkbox=True,
        true_label="Yes, I commit to carrying the certificate onboard",
        false_label="No, I cannot commit to this"
    )
    
    commitments_form.boolean_input_field(
        name="alternative_transport_available",
        label="I will ensure alternative accessible transport is available when needed for passengers who cannot use non-compliant vehicles",
        single_checkbox=True,
        true_label="Yes, I commit to providing alternative transport",
        false_label="No, I cannot commit to this"
    )
    
    commitments_form.boolean_input_field(
        name="written_confirmation_retained",
        label="I will retain written confirmation of alternative transport arrangements",
        single_checkbox=True,
        true_label="Yes, I commit to retaining written confirmation",
        false_label="No, I cannot commit to this"
    )
    
    # Connect form to flow
    user_flow.edge(START, commitments_form)
    user_flow.edge(commitments_form, END)
    
    # Map form outputs to flow outputs
    aflow.map_output(
        output_variable="will_carry_certificate_onboard",
        expression="flow['userflow_1']['operational_commitments_form'].output.will_carry_certificate_onboard"
    )
    aflow.map_output(
        output_variable="alternative_transport_available",
        expression="flow['userflow_1']['operational_commitments_form'].output.alternative_transport_available"
    )
    aflow.map_output(
        output_variable="written_confirmation_retained",
        expression="flow['userflow_1']['operational_commitments_form'].output.written_confirmation_retained"
    )
    
    # Check if all commitments are met
    aflow.map_output(
        output_variable="all_commitments_met",
        expression="flow['userflow_1']['operational_commitments_form'].output.will_carry_certificate_onboard and flow['userflow_1']['operational_commitments_form'].output.alternative_transport_available and flow['userflow_1']['operational_commitments_form'].output.written_confirmation_retained"
    )
    
    # Build list of missing commitments
    aflow.map_output(
        output_variable="missing_commitments",
        expression="[c for c in [('Carry exemption certificate onboard partially/non-compliant vehicles' if not flow['userflow_1']['operational_commitments_form'].output.will_carry_certificate_onboard else None), ('Provide alternative accessible transport when needed' if not flow['userflow_1']['operational_commitments_form'].output.alternative_transport_available else None), ('Retain written confirmation of alternative transport arrangements' if not flow['userflow_1']['operational_commitments_form'].output.written_confirmation_retained else None)] if c is not None]"
    )
    
    # Generate appropriate message
    aflow.map_output(
        output_variable="message",
        expression="('✓ Operational commitments recorded. All required commitments confirmed:\\n  • Will carry exemption certificate onboard\\n  • Alternative accessible transport will be available\\n  • Written confirmation will be retained\\n\\nData collection complete. Ready to proceed to final assessment.' if (flow['userflow_1']['operational_commitments_form'].output.will_carry_certificate_onboard and flow['userflow_1']['operational_commitments_form'].output.alternative_transport_available and flow['userflow_1']['operational_commitments_form'].output.written_confirmation_retained) else '✗ Operational commitments incomplete. All three commitments are REQUIRED for exemption eligibility. Without these commitments, the application cannot be approved.')"
    )
    
    # Define main flow sequence
    aflow.sequence(START, user_flow, END)
    
    return aflow

# Made with Bob