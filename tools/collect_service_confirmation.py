"""
Tool to collect service confirmation details for PSVAR exemption assessment.
This is Section 2 of the data collection process.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class ServiceConfirmation(BaseModel):
    """Service confirmation details"""
    is_hts_service: bool = Field(description="Whether this is a home-to-school (HTS) service")
    is_closed_door: bool = Field(description="Whether this is a closed-door service")
    has_paying_customers: bool = Field(description="Whether there are any paying customers")


class ServiceConfirmationOutput(BaseModel):
    """Output from service confirmation collection"""
    success: bool = Field(description="Whether collection was successful")
    message: str = Field(description="Confirmation message or error")
    data: ServiceConfirmation | None = Field(description="Collected service confirmation data", default=None)
    is_in_scope: bool = Field(description="Whether the service is in scope for PSVAR exemption")


@tool(permission=ToolPermission.READ_ONLY)
def collect_service_confirmation(
    is_hts_service: bool,
    is_closed_door: bool,
    has_paying_customers: bool
) -> ServiceConfirmationOutput:
    """
    Collect and validate service confirmation details for PSVAR exemption assessment.
    
    This is Section 2 of the data collection process. Call this tool after collecting
    company and contact information to confirm the service type and characteristics.
    
    IMPORTANT: Services are only in scope if:
    - Service type is HTS (home-to-school)
    - Service is closed-door
    - There are NO paying customers
    
    Args:
        is_hts_service: Is this a home-to-school (HTS) service? (true/false)
        is_closed_door: Is this a closed-door service? (true/false)
        has_paying_customers: Are there any paying customers? (true/false)
    
    Returns:
        ServiceConfirmationOutput with success status, scope determination, and collected data
    """
    
    # Store the collected information
    info = ServiceConfirmation(
        is_hts_service=is_hts_service,
        is_closed_door=is_closed_door,
        has_paying_customers=has_paying_customers
    )
    
    # Check if service is in scope
    is_in_scope = is_hts_service and is_closed_door and not has_paying_customers
    
    if not is_in_scope:
        # Determine why it's out of scope
        reasons = []
        if not is_hts_service:
            reasons.append("service is not home-to-school (HTS)")
        if not is_closed_door:
            reasons.append("service is not closed-door")
        if has_paying_customers:
            reasons.append("service has paying customers")
        
        reason_text = " and ".join(reasons)
        
        return ServiceConfirmationOutput(
            success=True,
            message=f"✗ Service is OUT OF SCOPE for PSVAR exemption because {reason_text}. PSVAR exemptions only apply to closed-door home-to-school services without paying customers.",
            data=info,
            is_in_scope=False
        )
    
    return ServiceConfirmationOutput(
        success=True,
        message="✓ Service confirmation recorded. Service is IN SCOPE for PSVAR exemption assessment. Ready to proceed to Section 3: Fleet Composition.",
        data=info,
        is_in_scope=True
    )

# Made with Bob
