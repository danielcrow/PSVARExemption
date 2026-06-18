"""
Flow to collect Vehicle Identification Numbers (VINs) for PSVAR exemption assessment.
This is Section 4 of the data collection process - presented as a form.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END


class VehicleVINsInput(BaseModel):
    """Input to start the VIN collection flow"""
    expected_total: int = Field(description="Expected total number of VINs")
    expected_partially_compliant: int = Field(description="Expected number of partially compliant VINs")
    expected_non_compliant: int = Field(description="Expected number of non-compliant VINs")


class VehicleVINsOutput(BaseModel):
    """Output from VIN collection"""
    all_vins_text: str = Field(description="All vehicle VINs as text (one per line)")
    partially_compliant_vins_text: str = Field(description="Partially compliant VINs as text (one per line)")
    non_compliant_vins_text: str = Field(description="Non-compliant VINs as text (one per line)")
    all_vins: list[str] = Field(description="All vehicle VINs as list")
    partially_compliant_vins: list[str] = Field(description="Partially compliant VINs as list")
    non_compliant_vins: list[str] = Field(description="Non-compliant VINs as list")
    validation_errors: list[str] = Field(description="Any validation errors found", default_factory=list)
    needs_operational_commitments: bool = Field(description="Whether operational commitments are needed")
    message: str = Field(description="Confirmation message or error")


@flow(
    name="collect_vehicle_vins",
    display_name="Section 4: Vehicle Identification Numbers",
    description="Collect vehicle VINs via form",
    input_schema=VehicleVINsInput,
    output_schema=VehicleVINsOutput
)
def build_collect_vehicle_vins(aflow: Flow) -> Flow:
    """
    CRITICAL: Flow function signature MUST be:
    def build_<flow_name>(aflow: Flow) -> Flow:
    """
    
    # Create user flow for form
    user_flow = aflow.userflow()
    user_flow.spec.display_name = "Vehicle Identification Numbers"
    
    # Create form
    vin_form = user_flow.form(
        name="vehicle_vins_form",
        display_name="Vehicle Identification Numbers (VINs)",
        instructions=f"Please provide the VINs for all vehicles in your fleet. VINs must be 8, 10, or 17 alphanumeric characters and cannot contain I, O, or Q. Enter one VIN per line.",
        submit_button_label="Continue to Section 5",
        cancel_button_label=None  # Hide cancel button
    )
    
    # Add form fields - using multi-line text areas for VIN lists
    vin_form.text_input_field(
        name="all_vins_text",
        label="All Vehicle VINs",
        required=True,
        single_line=False,
        placeholder_text="Enter one VIN per line\nExample:\n1HGBH41JXMN109186\n2HGFG12657H542890",
        help_text=f"Enter all {'{flow.input.expected_total}'} vehicle VINs, one per line (8, 10, or 17 characters each)"
    )
    
    vin_form.text_input_field(
        name="partially_compliant_vins_text",
        label="Partially Compliant Vehicle VINs",
        required=False,
        single_line=False,
        placeholder_text="Enter one VIN per line (if any)",
        help_text=f"Enter VINs for {'{flow.input.expected_partially_compliant}'} partially compliant vehicles, one per line"
    )
    
    vin_form.text_input_field(
        name="non_compliant_vins_text",
        label="Non-Compliant Vehicle VINs",
        required=False,
        single_line=False,
        placeholder_text="Enter one VIN per line (if any)",
        help_text=f"Enter VINs for {'{flow.input.expected_non_compliant}'} non-compliant vehicles, one per line"
    )
    
    # Connect form to flow
    user_flow.edge(START, vin_form)
    user_flow.edge(vin_form, END)
    
    # Map form outputs - store both text and parsed lists
    aflow.map_output(
        output_variable="all_vins_text",
        expression="flow['userflow_1']['vehicle_vins_form'].output.all_vins_text"
    )
    aflow.map_output(
        output_variable="partially_compliant_vins_text",
        expression="flow['userflow_1']['vehicle_vins_form'].output.partially_compliant_vins_text if flow['userflow_1']['vehicle_vins_form'].output.partially_compliant_vins_text else ''"
    )
    aflow.map_output(
        output_variable="non_compliant_vins_text",
        expression="flow['userflow_1']['vehicle_vins_form'].output.non_compliant_vins_text if flow['userflow_1']['vehicle_vins_form'].output.non_compliant_vins_text else ''"
    )
    
    # Parse VINs from text (split by newlines, strip whitespace, filter empty)
    aflow.map_output(
        output_variable="all_vins",
        expression="[vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()]"
    )
    aflow.map_output(
        output_variable="partially_compliant_vins",
        expression="[vin.strip().upper() for vin in (flow['userflow_1']['vehicle_vins_form'].output.partially_compliant_vins_text or '').split('\\n') if vin.strip()]"
    )
    aflow.map_output(
        output_variable="non_compliant_vins",
        expression="[vin.strip().upper() for vin in (flow['userflow_1']['vehicle_vins_form'].output.non_compliant_vins_text or '').split('\\n') if vin.strip()]"
    )
    
    # Basic validation - check VIN count matches expected
    aflow.map_output(
        output_variable="validation_errors",
        expression="[] if len([vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()]) == flow.input.expected_total else [f\"VIN count mismatch: Expected {flow.input.expected_total} VINs but received {len([vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()])}\"]"
    )
    
    # Determine if operational commitments are needed
    aflow.map_output(
        output_variable="needs_operational_commitments",
        expression="len([vin.strip().upper() for vin in (flow['userflow_1']['vehicle_vins_form'].output.partially_compliant_vins_text or '').split('\\n') if vin.strip()]) > 0 or len([vin.strip().upper() for vin in (flow['userflow_1']['vehicle_vins_form'].output.non_compliant_vins_text or '').split('\\n') if vin.strip()]) > 0"
    )
    
    # Generate appropriate message
    aflow.map_output(
        output_variable="message",
        expression="(f\"✗ VIN validation failed. VIN count mismatch: Expected {flow.input.expected_total} VINs but received {len([vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()])}. Please correct and try again.\" if len([vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()]) != flow.input.expected_total else (f\"✓ Vehicle VINs recorded. Collected {len([vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()])} VINs. Ready to proceed to Section 5: Operational Commitments.\" if (len([vin.strip().upper() for vin in (flow['userflow_1']['vehicle_vins_form'].output.partially_compliant_vins_text or '').split('\\n') if vin.strip()]) > 0 or len([vin.strip().upper() for vin in (flow['userflow_1']['vehicle_vins_form'].output.non_compliant_vins_text or '').split('\\n') if vin.strip()]) > 0) else f\"✓ Vehicle VINs recorded. Collected {len([vin.strip().upper() for vin in flow['userflow_1']['vehicle_vins_form'].output.all_vins_text.split('\\n') if vin.strip()])} VINs. All vehicles are fully compliant. Ready to proceed to final assessment.\"))"
    )
    
    # Define main flow sequence
    aflow.sequence(START, user_flow, END)
    
    return aflow

# Made with Bob