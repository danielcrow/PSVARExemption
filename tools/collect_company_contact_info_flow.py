"""
Flow to collect company and contact information for PSVAR exemption assessment.
This is Section 1 of the data collection process - presented as a form.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END


class CompanyContactInput(BaseModel):
    """Input to start the company contact collection flow"""
    pass


class CompanyContactOutput(BaseModel):
    """Output from company contact collection"""
    company_name: str = Field(description="Company or operator name")
    operator_licence_number: str = Field(description="Operator licence number")
    contact_name: str = Field(description="Authorized contact person's name")
    contact_phone: str = Field(description="Contact telephone number")
    contact_email: str = Field(description="Contact email address")
    postal_address: str = Field(description="Full postal address")
    postcode: str = Field(description="Postcode")
    message: str = Field(description="Confirmation message")


@flow(
    name="collect_company_contact_info",
    display_name="Section 1: Company & Contact Information",
    description="Collect company and contact information via form",
    input_schema=CompanyContactInput,
    output_schema=CompanyContactOutput
)
def build_collect_company_contact_info(aflow: Flow) -> Flow:
    """
    CRITICAL: Flow function signature MUST be:
    def build_<flow_name>(aflow: Flow) -> Flow:
    """
    
    # Create user flow for form
    user_flow = aflow.userflow()
    user_flow.spec.display_name = "Company & Contact Information"
    
    # Create form
    company_form = user_flow.form(
        name="company_contact_form",
        display_name="Company & Contact Information",
        instructions="Please provide your company and contact details",
        submit_button_label="Continue to Section 2",
        cancel_button_label=None  # Hide cancel button
    )
    
    # Add form fields
    company_form.text_input_field(
        name="company_name",
        label="Company/Operator Name",
        required=True,
        help_text="Full legal name of your company or organization"
    )
    
    company_form.text_input_field(
        name="operator_licence_number",
        label="Operator Licence Number",
        required=True,
        placeholder_text="e.g., OB1234567",
        help_text="Your PSV operator licence number"
    )
    
    company_form.text_input_field(
        name="contact_name",
        label="Authorized Contact Name",
        required=True,
        help_text="Full name of the person authorized to submit this application"
    )
    
    company_form.text_input_field(
        name="contact_phone",
        label="Contact Telephone",
        required=True,
        placeholder_text="e.g., 01234567890",
        help_text="Contact telephone number"
    )
    
    company_form.text_input_field(
        name="contact_email",
        label="Contact Email",
        required=True,
        placeholder_text="e.g., contact@company.com",
        help_text="Contact email address"
    )
    
    company_form.text_input_field(
        name="postal_address",
        label="Postal Address",
        required=True,
        single_line=False,
        help_text="Full postal address (street, city, etc.)"
    )
    
    company_form.text_input_field(
        name="postcode",
        label="Postcode",
        required=True,
        placeholder_text="e.g., SW1A 1AA",
        help_text="UK postcode"
    )
    
    # Connect form to flow
    user_flow.edge(START, company_form)
    user_flow.edge(company_form, END)
    
    # Map form outputs to flow outputs
    aflow.map_output(
        output_variable="company_name",
        expression="flow['userflow_1']['company_contact_form'].output.company_name"
    )
    aflow.map_output(
        output_variable="operator_licence_number",
        expression="flow['userflow_1']['company_contact_form'].output.operator_licence_number"
    )
    aflow.map_output(
        output_variable="contact_name",
        expression="flow['userflow_1']['company_contact_form'].output.contact_name"
    )
    aflow.map_output(
        output_variable="contact_phone",
        expression="flow['userflow_1']['company_contact_form'].output.contact_phone"
    )
    aflow.map_output(
        output_variable="contact_email",
        expression="flow['userflow_1']['company_contact_form'].output.contact_email"
    )
    aflow.map_output(
        output_variable="postal_address",
        expression="flow['userflow_1']['company_contact_form'].output.postal_address"
    )
    aflow.map_output(
        output_variable="postcode",
        expression="flow['userflow_1']['company_contact_form'].output.postcode"
    )
    aflow.map_output(
        output_variable="message",
        expression="'✓ Company and contact information recorded for ' + (flow['userflow_1']['company_contact_form'].output.company_name or 'Unknown') + '. Ready to proceed to Section 2: Service Confirmation.'"
    )
    
    # Define main flow sequence
    aflow.sequence(START, user_flow, END)
    
    return aflow

# Made with Bob
