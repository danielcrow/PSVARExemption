"""
Flow to collect service confirmation details for PSVAR exemption assessment.
This is Section 2 of the data collection process - presented as a form.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END


class ServiceConfirmationInput(BaseModel):
    """Input to start the service confirmation collection flow"""
    pass


class ServiceConfirmationOutput(BaseModel):
    """Output from service confirmation collection"""
    is_hts_service: bool = Field(description="Whether this is a home-to-school (HTS) service")
    is_closed_door: bool = Field(description="Whether this is a closed-door service")
    has_paying_customers: bool = Field(description="Whether there ARE paying customers (true means has paying customers, false means no paying customers)")
    is_in_scope: bool = Field(description="Whether the service is in scope for PSVAR exemption")
    message: str = Field(description="Confirmation message")


@flow(
    name="collect_service_confirmation",
    display_name="Section 2: Service Confirmation",
    description="Collect service confirmation details via form",
    input_schema=ServiceConfirmationInput,
    output_schema=ServiceConfirmationOutput
)
def build_collect_service_confirmation(aflow: Flow) -> Flow:
    """
    CRITICAL: Flow function signature MUST be:
    def build_<flow_name>(aflow: Flow) -> Flow:
    """
    
    # Create user flow for form
    user_flow = aflow.userflow()
    user_flow.spec.display_name = "Service Confirmation"
    
    # Create form
    service_form = user_flow.form(
        name="service_confirmation_form",
        display_name="Service Confirmation",
        instructions="Please confirm the characteristics of your service. PSVAR exemptions only apply to closed-door home-to-school services without paying customers.",
        submit_button_label="Continue to Section 3",
        cancel_button_label=None  # Hide cancel button
    )
    
    # Add form fields
    service_form.boolean_input_field(
        name="is_hts_service",
        label="✓ This is a home-to-school (HTS) service"
    )
    
    service_form.boolean_input_field(
        name="is_closed_door",
        label="✓ This is a closed-door service (only for specific passengers)"
    )
    
    service_form.boolean_input_field(
        name="has_no_paying_customers_checkbox",
        label="✓ This service has NO paying customers (free service)"
    )
    
    # Connect form to flow
    user_flow.edge(START, service_form)
    user_flow.edge(service_form, END)
    
    # Map outputs - INVERT the checkbox value for has_paying_customers
    # Checkbox checked (True) = NO paying customers = has_paying_customers should be False
    # Checkbox unchecked (False) = HAS paying customers = has_paying_customers should be True
    aflow.map_output(
        output_variable="is_hts_service",
        expression="flow['userflow_1']['service_confirmation_form'].output.is_hts_service"
    )
    aflow.map_output(
        output_variable="is_closed_door",
        expression="flow['userflow_1']['service_confirmation_form'].output.is_closed_door"
    )
    aflow.map_output(
        output_variable="has_paying_customers",
        expression="not bool(flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers_checkbox)"
    )
    
    # Calculate in_scope status (service is in scope when it's HTS, closed door, and has NO paying customers)
    # Which means: is_hts_service=True AND is_closed_door=True AND has_paying_customers=False
    aflow.map_output(
        output_variable="is_in_scope",
        expression="bool(flow['userflow_1']['service_confirmation_form'].output.is_hts_service) and bool(flow['userflow_1']['service_confirmation_form'].output.is_closed_door) and bool(flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers_checkbox)"
    )
    
    # Generate appropriate message based on scope
    aflow.map_output(
        output_variable="message",
        expression="('✓ Service confirmation recorded. Service is IN SCOPE for PSVAR exemption assessment. Ready to proceed to Section 3: Fleet Composition.' if (flow['userflow_1']['service_confirmation_form'].output.is_hts_service and flow['userflow_1']['service_confirmation_form'].output.is_closed_door and flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers_checkbox) else '✗ Service is OUT OF SCOPE for PSVAR exemption. PSVAR exemptions only apply to closed-door home-to-school services without paying customers.')"
    )
    
    # Define main flow sequence
    aflow.sequence(START, user_flow, END)
    
    return aflow

# Made with Bob