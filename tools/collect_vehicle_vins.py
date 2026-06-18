"""
Tool to collect Vehicle Identification Numbers (VINs) for PSVAR exemption assessment.
This is Section 4 of the data collection process.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class VehicleVINs(BaseModel):
    """Vehicle Identification Numbers"""
    all_vins: list[str] = Field(description="All vehicle VINs")
    partially_compliant_vins: list[str] = Field(description="VINs of partially compliant vehicles")
    non_compliant_vins: list[str] = Field(description="VINs of non-compliant vehicles")


class VehicleVINsOutput(BaseModel):
    """Output from VIN collection"""
    success: bool = Field(description="Whether collection was successful")
    message: str = Field(description="Confirmation message or error")
    data: VehicleVINs | None = Field(description="Collected VIN data", default=None)
    validation_errors: list[str] = Field(description="Any validation errors found", default_factory=list)
    needs_operational_commitments: bool = Field(description="Whether operational commitments are needed", default=False)


def validate_vin_format(vin: str) -> bool:
    """Basic VIN format validation (8, 10, or 17 characters, alphanumeric, no I/O/Q)"""
    # VINs can be 8, 10, or 17 characters
    if len(vin) not in [8, 10, 17]:
        return False
    if not vin.isalnum():
        return False
    # VINs don't use I, O, or Q to avoid confusion with 1 and 0
    if any(char in vin.upper() for char in ['I', 'O', 'Q']):
        return False
    return True


@tool(permission=ToolPermission.READ_ONLY)
def collect_vehicle_vins(
    all_vins: list[str],
    partially_compliant_vins: list[str] | None = None,
    non_compliant_vins: list[str] | None = None,
    expected_total: int | None = None,
    expected_partially_compliant: int | None = None,
    expected_non_compliant: int | None = None
) -> VehicleVINsOutput:
    """
    Collect and validate Vehicle Identification Numbers (VINs) for PSVAR exemption assessment.
    
    This is Section 4 of the data collection process. Call this tool after collecting
    fleet composition to record all vehicle VINs and categorize them by compliance status.
    
    VIN Requirements:
    - Must be 8, 10, or 17 characters
    - Alphanumeric only
    - Cannot contain I, O, or Q (to avoid confusion with 1 and 0)
    
    Args:
        all_vins: List of all vehicle VINs (17 characters each)
        partially_compliant_vins: List of VINs for partially compliant vehicles (optional)
        non_compliant_vins: List of VINs for non-compliant vehicles (optional)
        expected_total: Expected total number of VINs (for validation)
        expected_partially_compliant: Expected number of partially compliant VINs
        expected_non_compliant: Expected number of non-compliant VINs
    
    Returns:
        VehicleVINsOutput with success status, validation results, and collected data
    """
    
    validation_errors = []
    partially_compliant_vins = partially_compliant_vins or []
    non_compliant_vins = non_compliant_vins or []
    
    # Validate VIN count matches expected total
    if expected_total is not None and len(all_vins) != expected_total:
        validation_errors.append(
            f"VIN count mismatch: Expected {expected_total} VINs but received {len(all_vins)}"
        )
    
    # Validate VIN format
    invalid_vins = []
    for vin in all_vins:
        if not validate_vin_format(vin):
            invalid_vins.append(vin)
    
    if invalid_vins:
        validation_errors.append(
            f"Invalid VIN format for: {', '.join(invalid_vins)}. VINs must be 8, 10, or 17 alphanumeric characters and cannot contain I, O, or Q."
        )
    
    # Check for duplicate VINs
    if len(all_vins) != len(set(all_vins)):
        duplicates = [vin for vin in all_vins if all_vins.count(vin) > 1]
        unique_duplicates = list(set(duplicates))
        validation_errors.append(
            f"Duplicate VINs found: {', '.join(unique_duplicates)}"
        )
    
    # Validate partially compliant VINs are in all_vins
    invalid_partial = [vin for vin in partially_compliant_vins if vin not in all_vins]
    if invalid_partial:
        validation_errors.append(
            f"Partially compliant VINs not found in all VINs: {', '.join(invalid_partial)}"
        )
    
    # Validate non-compliant VINs are in all_vins
    invalid_non = [vin for vin in non_compliant_vins if vin not in all_vins]
    if invalid_non:
        validation_errors.append(
            f"Non-compliant VINs not found in all VINs: {', '.join(invalid_non)}"
        )
    
    # Validate counts match expected
    if expected_partially_compliant is not None and len(partially_compliant_vins) != expected_partially_compliant:
        validation_errors.append(
            f"Partially compliant VIN count mismatch: Expected {expected_partially_compliant} but received {len(partially_compliant_vins)}"
        )
    
    if expected_non_compliant is not None and len(non_compliant_vins) != expected_non_compliant:
        validation_errors.append(
            f"Non-compliant VIN count mismatch: Expected {expected_non_compliant} but received {len(non_compliant_vins)}"
        )
    
    # Check for VINs in both partially and non-compliant lists
    overlap = set(partially_compliant_vins) & set(non_compliant_vins)
    if overlap:
        validation_errors.append(
            f"VINs cannot be both partially compliant and non-compliant: {', '.join(overlap)}"
        )
    
    # If there are validation errors, return them
    if validation_errors:
        return VehicleVINsOutput(
            success=False,
            message="✗ VIN validation failed. Please correct the errors and try again.",
            data=None,
            validation_errors=validation_errors,
            needs_operational_commitments=False
        )
    
    # Store the collected information
    info = VehicleVINs(
        all_vins=all_vins,
        partially_compliant_vins=partially_compliant_vins,
        non_compliant_vins=non_compliant_vins
    )
    
    # Determine if operational commitments are needed
    needs_commitments = len(partially_compliant_vins) > 0 or len(non_compliant_vins) > 0
    
    # Build message
    message = f"✓ Vehicle VINs recorded. Collected {len(all_vins)} VINs"
    if partially_compliant_vins:
        message += f", {len(partially_compliant_vins)} partially compliant"
    if non_compliant_vins:
        message += f", {len(non_compliant_vins)} non-compliant"
    message += ". "
    
    if needs_commitments:
        message += "Ready to proceed to Section 5: Operational Commitments."
    else:
        message += "All vehicles are fully compliant. Ready to proceed to final assessment."
    
    return VehicleVINsOutput(
        success=True,
        message=message,
        data=info,
        validation_errors=[],
        needs_operational_commitments=needs_commitments
    )

# Made with Bob
