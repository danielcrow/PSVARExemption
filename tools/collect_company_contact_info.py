"""
Tool to collect company and contact information for PSVAR exemption assessment.
This is Section 1 of the data collection process.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class CompanyContactInfo(BaseModel):
    """Company and contact information"""
    company_name: str = Field(description="Company or operator name")
    operator_licence_number: str = Field(description="Operator licence number")
    contact_name: str = Field(description="Authorized contact person's name")
    contact_phone: str = Field(description="Contact telephone number")
    contact_email: str = Field(description="Contact email address")
    postal_address: str = Field(description="Full postal address")
    postcode: str = Field(description="Postcode")


class CompanyContactOutput(BaseModel):
    """Output from company contact collection"""
    success: bool = Field(description="Whether collection was successful")
    message: str = Field(description="Confirmation message")
    data: CompanyContactInfo = Field(description="Collected company and contact information")


@tool(permission=ToolPermission.READ_ONLY)
def collect_company_contact_info(
    company_name: str,
    operator_licence_number: str,
    contact_name: str,
    contact_phone: str,
    contact_email: str,
    postal_address: str,
    postcode: str
) -> CompanyContactOutput:
    """
    Collect and validate company and contact information for PSVAR exemption assessment.
    
    This is Section 1 of the data collection process. Call this tool first to record
    the company and contact details before proceeding to service confirmation.
    
    Args:
        company_name: Company or operator name
        operator_licence_number: Operator licence number (e.g., OB1234567)
        contact_name: Authorized contact person's full name
        contact_phone: Contact telephone number
        contact_email: Contact email address
        postal_address: Full postal address (street, city)
        postcode: UK postcode
    
    Returns:
        CompanyContactOutput with success status and collected data
    """
    
    # Store the collected information
    info = CompanyContactInfo(
        company_name=company_name,
        operator_licence_number=operator_licence_number,
        contact_name=contact_name,
        contact_phone=contact_phone,
        contact_email=contact_email,
        postal_address=postal_address,
        postcode=postcode
    )
    
    return CompanyContactOutput(
        success=True,
        message=f"✓ Company and contact information recorded for {company_name}. Ready to proceed to Section 2: Service Confirmation.",
        data=info
    )

# Made with Bob
