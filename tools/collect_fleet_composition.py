"""
Tool to collect fleet composition details for PSVAR exemption assessment.
This is Section 3 of the data collection process.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class FleetComposition(BaseModel):
    """Fleet composition details"""
    total_fleet_size: int = Field(description="Total number of HTS vehicles")
    fully_compliant_count: int = Field(description="Number of fully compliant vehicles")
    partially_compliant_count: int = Field(description="Number of partially compliant vehicles")
    non_compliant_count: int = Field(description="Number of non-compliant vehicles")
    band: str = Field(description="Compliance band (A, B, C, or D)")
    has_read_band_requirements: bool = Field(description="Whether applicant has read band requirements")


class FleetCompositionOutput(BaseModel):
    """Output from fleet composition collection"""
    success: bool = Field(description="Whether collection was successful")
    message: str = Field(description="Confirmation message or error")
    data: FleetComposition | None = Field(description="Collected fleet composition data", default=None)
    validation_errors: list[str] = Field(description="Any validation errors found", default_factory=list)


def calculate_band(fleet_size: int) -> str:
    """Calculate compliance band based on fleet size"""
    if fleet_size <= 5:
        return "A"
    elif fleet_size <= 9:
        return "B"
    elif fleet_size <= 29:
        return "C"
    else:
        return "D"


@tool(permission=ToolPermission.READ_ONLY)
def collect_fleet_composition(
    total_fleet_size: int,
    fully_compliant_count: int,
    partially_compliant_count: int,
    non_compliant_count: int,
    has_read_band_requirements: bool
) -> FleetCompositionOutput:
    """
    Collect and validate fleet composition details for PSVAR exemption assessment.
    
    This is Section 3 of the data collection process. Call this tool after confirming
    the service is in scope to record fleet composition and determine the compliance band.
    
    Compliance Bands:
    - Band A: 1-5 vehicles
    - Band B: 6-9 vehicles
    - Band C: 10-29 vehicles
    - Band D: 30+ vehicles
    
    Args:
        total_fleet_size: Total number of HTS vehicles in the fleet
        fully_compliant_count: Number of fully compliant vehicles (Schedule 1 + Schedule 3)
        partially_compliant_count: Number of partially compliant vehicles (Schedule 3 only)
        non_compliant_count: Number of non-compliant vehicles (neither schedule)
        has_read_band_requirements: Has the applicant read the band compliance requirements?
    
    Returns:
        FleetCompositionOutput with success status, band determination, and collected data
    """
    
    validation_errors = []
    
    # Validate that counts add up to total
    total_from_counts = fully_compliant_count + partially_compliant_count + non_compliant_count
    if total_from_counts != total_fleet_size:
        validation_errors.append(
            f"Fleet size mismatch: Total fleet size is {total_fleet_size}, but vehicle counts add up to {total_from_counts}. "
            f"Please verify: {fully_compliant_count} fully compliant + {partially_compliant_count} partially compliant + "
            f"{non_compliant_count} non-compliant = {total_from_counts}"
        )
    
    # Validate positive numbers
    if total_fleet_size <= 0:
        validation_errors.append("Total fleet size must be greater than 0")
    if fully_compliant_count < 0 or partially_compliant_count < 0 or non_compliant_count < 0:
        validation_errors.append("Vehicle counts cannot be negative")
    
    # If there are validation errors, return them
    if validation_errors:
        return FleetCompositionOutput(
            success=False,
            message="✗ Fleet composition validation failed. Please correct the errors and try again.",
            data=None,
            validation_errors=validation_errors
        )
    
    # Calculate band
    band = calculate_band(total_fleet_size)
    
    # Check if all vehicles are fully compliant
    all_compliant = fully_compliant_count == total_fleet_size
    
    # Store the collected information
    info = FleetComposition(
        total_fleet_size=total_fleet_size,
        fully_compliant_count=fully_compliant_count,
        partially_compliant_count=partially_compliant_count,
        non_compliant_count=non_compliant_count,
        band=band,
        has_read_band_requirements=has_read_band_requirements
    )
    
    # Build message
    if all_compliant:
        message = (
            f"✓ Fleet composition recorded. Your fleet is in Band {band} ({total_fleet_size} vehicles). "
            f"All {total_fleet_size} vehicles are fully compliant with PSVAR - no exemption needed! "
            f"You can proceed directly to operating your service."
        )
    else:
        message = (
            f"✓ Fleet composition recorded. Your fleet is in Band {band} ({total_fleet_size} vehicles): "
            f"{fully_compliant_count} fully compliant, {partially_compliant_count} partially compliant, "
            f"{non_compliant_count} non-compliant. "
        )
        if has_read_band_requirements:
            message += f"You have confirmed reading Band {band} requirements. Ready to proceed to Section 4: Vehicle Identification Numbers."
        else:
            message += f"⚠️ You must read and understand Band {band} requirements before proceeding."
    
    return FleetCompositionOutput(
        success=True,
        message=message,
        data=info,
        validation_errors=[]
    )

# Made with Bob
