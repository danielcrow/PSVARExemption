"""
Flow to collect fleet composition details for PSVAR exemption assessment.
This is Section 3 of the data collection process - presented as a form.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END


class FleetCompositionInput(BaseModel):
    """Input to start the fleet composition collection flow"""
    pass


class FleetCompositionOutput(BaseModel):
    """Output from fleet composition collection"""
    total_fleet_size: int = Field(description="Total number of HTS vehicles")
    fully_compliant_count: int = Field(description="Number of fully compliant vehicles")
    partially_compliant_count: int = Field(description="Number of partially compliant vehicles")
    non_compliant_count: int = Field(description="Number of non-compliant vehicles")
    band: str = Field(description="Compliance band (A, B, C, or D)")
    has_read_band_requirements: bool = Field(description="Whether applicant has read band requirements")
    validation_errors: list[str] = Field(description="Any validation errors found", default_factory=list)
    message: str = Field(description="Confirmation message or error")


@flow(
    name="collect_fleet_composition",
    display_name="Section 3: Fleet Composition",
    description="Collect fleet composition details via form",
    input_schema=FleetCompositionInput,
    output_schema=FleetCompositionOutput
)
def build_collect_fleet_composition(aflow: Flow) -> Flow:
    """
    CRITICAL: Flow function signature MUST be:
    def build_<flow_name>(aflow: Flow) -> Flow:
    """
    
    # Create user flow for form
    user_flow = aflow.userflow()
    user_flow.spec.display_name = "Fleet Composition"
    
    # Create form
    fleet_form = user_flow.form(
        name="fleet_composition_form",
        display_name="Fleet Composition",
        instructions="Please provide details about your fleet composition. All vehicles must be categorized as fully compliant, partially compliant, or non-compliant.",
        submit_button_label="Continue to Section 4",
        cancel_button_label=None  # Hide cancel button
    )
    
    # Add form fields
    fleet_form.number_input_field(
        name="total_fleet_size",
        label="Total Fleet Size",
        required=True,
        is_integer=True,
        help_text="Total number of vehicles used for home-to-school services"
    )
    
    fleet_form.number_input_field(
        name="fully_compliant_count",
        label="Fully Compliant Vehicles",
        required=True,
        is_integer=True,
        help_text="Number of vehicles that comply with both Schedule 1 (wheelchair facilities) and Schedule 3 (other accessibility features)"
    )
    
    fleet_form.number_input_field(
        name="partially_compliant_count",
        label="Partially Compliant Vehicles",
        required=True,
        is_integer=True,
        help_text="Number of vehicles that comply with Schedule 3 only (floors, seats, steps, handrails)"
    )
    
    fleet_form.number_input_field(
        name="non_compliant_count",
        label="Non-Compliant Vehicles",
        required=True,
        is_integer=True,
        help_text="Number of vehicles that do not meet compliance requirements"
    )
    
    fleet_form.boolean_input_field(
        name="has_read_band_requirements",
        label="I have read and understand the compliance band requirements for my fleet size",
        single_checkbox=True,
        true_label="Yes, I have read the requirements",
        false_label="No, I have not read the requirements"
    )
    
    # Connect form to flow
    user_flow.edge(START, fleet_form)
    user_flow.edge(fleet_form, END)
    
    # Map form outputs to flow outputs
    aflow.map_output(
        output_variable="total_fleet_size",
        expression="flow['userflow_1']['fleet_composition_form'].output.total_fleet_size"
    )
    aflow.map_output(
        output_variable="fully_compliant_count",
        expression="flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count"
    )
    aflow.map_output(
        output_variable="partially_compliant_count",
        expression="flow['userflow_1']['fleet_composition_form'].output.partially_compliant_count"
    )
    aflow.map_output(
        output_variable="non_compliant_count",
        expression="flow['userflow_1']['fleet_composition_form'].output.non_compliant_count"
    )
    aflow.map_output(
        output_variable="has_read_band_requirements",
        expression="flow['userflow_1']['fleet_composition_form'].output.has_read_band_requirements"
    )
    
    # Calculate band based on fleet size
    # Band A: 1-5, Band B: 6-9, Band C: 10-29, Band D: 30+
    aflow.map_output(
        output_variable="band",
        expression="'A' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 5 else ('B' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 9 else ('C' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 29 else 'D'))"
    )
    
    # Validate that counts add up to total (using list comprehension for validation)
    aflow.map_output(
        output_variable="validation_errors",
        expression="[] if (flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count + flow['userflow_1']['fleet_composition_form'].output.partially_compliant_count + flow['userflow_1']['fleet_composition_form'].output.non_compliant_count == flow['userflow_1']['fleet_composition_form'].output.total_fleet_size) else [f\"Fleet size mismatch: Total fleet size is {flow['userflow_1']['fleet_composition_form'].output.total_fleet_size}, but vehicle counts add up to {flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count + flow['userflow_1']['fleet_composition_form'].output.partially_compliant_count + flow['userflow_1']['fleet_composition_form'].output.non_compliant_count}\"]"
    )
    
    # Generate appropriate message
    aflow.map_output(
        output_variable="message",
        expression="(f\"✗ Fleet composition validation failed. Fleet size mismatch: Total fleet size is {flow['userflow_1']['fleet_composition_form'].output.total_fleet_size}, but vehicle counts add up to {flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count + flow['userflow_1']['fleet_composition_form'].output.partially_compliant_count + flow['userflow_1']['fleet_composition_form'].output.non_compliant_count}. Please correct and try again.\" if (flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count + flow['userflow_1']['fleet_composition_form'].output.partially_compliant_count + flow['userflow_1']['fleet_composition_form'].output.non_compliant_count != flow['userflow_1']['fleet_composition_form'].output.total_fleet_size) else (f\"✓ Fleet composition recorded. Your fleet is in Band {'A' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 5 else ('B' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 9 else ('C' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 29 else 'D'))} ({flow['userflow_1']['fleet_composition_form'].output.total_fleet_size} vehicles). All vehicles are fully compliant - no exemption needed!\" if flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count == flow['userflow_1']['fleet_composition_form'].output.total_fleet_size else f\"✓ Fleet composition recorded. Your fleet is in Band {'A' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 5 else ('B' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 9 else ('C' if flow['userflow_1']['fleet_composition_form'].output.total_fleet_size <= 29 else 'D'))} ({flow['userflow_1']['fleet_composition_form'].output.total_fleet_size} vehicles): {flow['userflow_1']['fleet_composition_form'].output.fully_compliant_count} fully compliant, {flow['userflow_1']['fleet_composition_form'].output.partially_compliant_count} partially compliant, {flow['userflow_1']['fleet_composition_form'].output.non_compliant_count} non-compliant. Ready to proceed to Section 4: Vehicle Identification Numbers.\"))"
    )
    
    # Define main flow sequence
    aflow.sequence(START, user_flow, END)
    
    return aflow

# Made with Bob