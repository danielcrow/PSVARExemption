"""
Tool to collect operational commitments for PSVAR exemption assessment.
This is Section 5 of the data collection process (only needed if partially/non-compliant vehicles exist).
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class OperationalCommitments(BaseModel):
    """Operational commitments for partially/non-compliant vehicles"""
    will_carry_certificate_onboard: bool = Field(
        description="Will carry exemption certificate onboard partially/non-compliant vehicles"
    )
    alternative_transport_available: bool = Field(
        description="Alternative accessible transport will be available when needed"
    )
    written_confirmation_retained: bool = Field(
        description="Will retain written confirmation of alternative transport arrangements"
    )


class OperationalCommitmentsOutput(BaseModel):
    """Output from operational commitments collection"""
    success: bool = Field(description="Whether collection was successful")
    message: str = Field(description="Confirmation message")
    data: OperationalCommitments = Field(description="Collected operational commitments")
    all_commitments_met: bool = Field(description="Whether all required commitments are met")
    missing_commitments: list[str] = Field(description="List of missing commitments", default_factory=list)


@tool(permission=ToolPermission.READ_ONLY)
def collect_operational_commitments(
    will_carry_certificate_onboard: bool,
    alternative_transport_available: bool,
    written_confirmation_retained: bool
) -> OperationalCommitmentsOutput:
    """
    Collect operational commitments for PSVAR exemption assessment.
    
    This is Section 5 of the data collection process. Call this tool ONLY if the fleet
    contains partially compliant or non-compliant vehicles. These commitments are
    REQUIRED for exemption eligibility.
    
    Required Commitments:
    1. Must carry a copy of the exemption certificate onboard each partially/non-compliant vehicle
    2. Must have alternative accessible transport available when needed
    3. Must retain written confirmation of alternative transport arrangements
    
    ALL THREE commitments must be "yes" (true) for exemption eligibility.
    
    Args:
        will_carry_certificate_onboard: Will you carry exemption certificate onboard? (true/false)
        alternative_transport_available: Will alternative accessible transport be available? (true/false)
        written_confirmation_retained: Will you retain written confirmation? (true/false)
    
    Returns:
        OperationalCommitmentsOutput with success status and commitment validation
    """
    
    # Store the collected information
    info = OperationalCommitments(
        will_carry_certificate_onboard=will_carry_certificate_onboard,
        alternative_transport_available=alternative_transport_available,
        written_confirmation_retained=written_confirmation_retained
    )
    
    # Check which commitments are missing
    missing = []
    if not will_carry_certificate_onboard:
        missing.append("Carry exemption certificate onboard partially/non-compliant vehicles")
    if not alternative_transport_available:
        missing.append("Provide alternative accessible transport when needed")
    if not written_confirmation_retained:
        missing.append("Retain written confirmation of alternative transport arrangements")
    
    all_met = len(missing) == 0
    
    # Build message
    if all_met:
        message = (
            "✓ Operational commitments recorded. All required commitments confirmed:\n"
            "  • Will carry exemption certificate onboard\n"
            "  • Alternative accessible transport will be available\n"
            "  • Written confirmation will be retained\n\n"
            "Data collection complete. Ready to proceed to final assessment."
        )
    else:
        message = (
            "✗ Operational commitments incomplete. The following required commitments are missing:\n"
            + "\n".join(f"  • {item}" for item in missing) +
            "\n\nAll three commitments are REQUIRED for exemption eligibility. "
            "Without these commitments, the application cannot be approved."
        )
    
    return OperationalCommitmentsOutput(
        success=True,
        message=message,
        data=info,
        all_commitments_met=all_met,
        missing_commitments=missing
    )

# Made with Bob
