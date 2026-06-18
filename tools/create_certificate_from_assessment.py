"""
Tool to create PSVAR exemption certificate from assessment data.
Bridges the PSVARAssessmentInput data structure with certificate generation.
"""

from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class VehicleEntry(BaseModel):
    """Single vehicle entry for Schedule B"""
    registration: str = Field(description="Vehicle registration number")
    vin: str = Field(description="Vehicle Identification Number (VIN/Chassis Number)")


class AssessmentToCertificateInput(BaseModel):
    """Input data from PSVAR assessment to generate certificate"""
    # From PSVARAssessmentInput
    company_name: str = Field(description="Operator/company name")
    operator_licence_number: str = Field(description="Operator licence number")
    authorised_contact_name: str | None = Field(default=None, description="Contact name")
    authorised_contact_email: str | None = Field(default=None, description="Contact email")
    authorised_contact_postal_address: str | None = Field(default=None, description="Postal address")
    authorised_contact_postcode: str | None = Field(default=None, description="Postcode")
    
    # Fleet data from 1st May 2026
    in_scope_compliant_coaches_may_2026: int = Field(
        description="Fully PSVAR compliant coaches on 1st May 2026 for HTS/RR services"
    )
    all_coaches_may_2026: int = Field(
        description="Total coaches on 1st May 2026 (all services)"
    )
    
    # Current fleet composition
    total_hts_rr_fleet_size: int = Field(description="Total HTS fleet size")
    fully_compliant_vehicle_count: int = Field(description="Fully compliant vehicles")
    partially_compliant_vehicle_count: int = Field(description="Partially compliant vehicles")
    non_compliant_vehicle_count: int = Field(description="Non-compliant vehicles")
    
    # Vehicle VINs - for non-compliant and partially compliant vehicles
    partially_compliant_vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for partially compliant vehicles"
    )
    non_compliant_vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for non-compliant vehicles"
    )
    
    # Vehicle registrations (optional - if not provided, will use placeholder)
    vehicle_registrations: list[str] | None = Field(
        default=None,
        description="Vehicle registration numbers corresponding to VINs"
    )
    
    # Compliance band
    compliance_band: str = Field(description="Compliance band: A, B, C, or D")
    
    # Certificate details (optional - will use defaults if not provided)
    service_reference: str | None = Field(
        default=None,
        description="Service reference (will be auto-generated if not provided)"
    )
    issue_date: str | None = Field(
        default=None,
        description="Issue date DD/MM/YYYY (defaults to today)"
    )
    expiry_date: str | None = Field(
        default=None,
        description="Expiry date DD/MM/YYYY (defaults to 2 years from issue)"
    )


class CertificateGenerationOutput(BaseModel):
    """Output from certificate generation"""
    success: bool = Field(description="Whether generation was successful")
    certificate_text: str = Field(description="Complete formatted certificate text")
    certificate_summary: str = Field(description="Brief summary of certificate")
    service_reference: str = Field(description="Service reference number")
    minimum_fleet_proportion: float = Field(description="Minimum fleet proportion percentage")
    is_valid_immediately: bool = Field(description="Whether certificate is valid immediately")
    validity_status: str = Field(description="Certificate validity status message")
    issue_date: str = Field(description="Certificate issue date")
    expiry_date: str = Field(description="Certificate expiry date")
    vehicle_count: int = Field(description="Number of vehicles covered")
    band: str = Field(description="Compliance band")
    calculation_details: dict = Field(description="Schedule A calculation details")


@tool(permission=ToolPermission.READ_ONLY)
def create_certificate_from_assessment(
    assessment_data: AssessmentToCertificateInput
) -> CertificateGenerationOutput:
    """
    Generate a PSVAR exemption certificate from assessment data.
    
    Takes the data collected during PSVAR assessment and generates a complete
    exemption certificate including all required sections, schedules, and legal text.
    
    Args:
        assessment_data: Assessment data including operator details, fleet composition,
                        and compliance information
    
    Returns:
        CertificateGenerationOutput with complete certificate text and metadata
    """
    
    # Calculate minimum fleet proportion using Schedule A logic
    in_scope_coaches = assessment_data.in_scope_compliant_coaches_may_2026
    all_coaches = assessment_data.all_coaches_may_2026
    
    # Calculate actual proportion
    actual_proportion = (in_scope_coaches / all_coaches) * 100 if all_coaches > 0 else 0
    
    # Determine MTE minimum requirement based on in-scope fleet size
    # Using total_hts_rr_fleet_size as proxy for in-scope coaches on 1st May 2026
    in_scope_total = assessment_data.total_hts_rr_fleet_size
    
    if in_scope_total <= 5:
        mte_minimum_coaches = 1
    elif in_scope_total <= 9:
        mte_minimum_coaches = 2
    elif in_scope_total <= 29:
        mte_minimum_coaches = max(1, int((in_scope_total * 0.25) + 0.999))  # Round up
    else:
        mte_minimum_coaches = max(1, int((in_scope_total * 0.35) + 0.999))  # Round up
    
    # Calculate MTE minimum proportion
    mte_minimum_proportion = (mte_minimum_coaches / all_coaches) * 100 if all_coaches > 0 else 0
    
    # Select higher proportion
    minimum_fleet_proportion = max(actual_proportion, mte_minimum_proportion)
    
    # Check if operator was MTE compliant on 1st May 2026
    was_mte_compliant = in_scope_coaches >= mte_minimum_coaches
    
    # Generate service reference if not provided
    service_reference = assessment_data.service_reference or f"PSVAR-{datetime.now().year}-{assessment_data.operator_licence_number}"
    
    # Set dates
    issue_date_str = assessment_data.issue_date or datetime.now().strftime("%d/%m/%Y")
    if assessment_data.expiry_date:
        expiry_date_str = assessment_data.expiry_date
    else:
        expiry_dt = datetime.now() + timedelta(days=730)  # 2 years
        expiry_date_str = expiry_dt.strftime("%d/%m/%Y")
    
    # Prepare vehicle list for Schedule B
    # Combine partially compliant and non-compliant vehicles
    all_vins = (
        assessment_data.partially_compliant_vehicle_identification_numbers +
        assessment_data.non_compliant_vehicle_identification_numbers
    )
    
    # Generate registrations if not provided
    if assessment_data.vehicle_registrations and len(assessment_data.vehicle_registrations) == len(all_vins):
        registrations = assessment_data.vehicle_registrations
    else:
        # Generate placeholder registrations
        registrations = [f"REG{i+1:04d}" for i in range(len(all_vins))]
    
    # Build Schedule B table
    schedule_b_rows = []
    for reg, vin in zip(registrations, all_vins):
        schedule_b_rows.append(
            f"{assessment_data.company_name} | {assessment_data.operator_licence_number} | {reg} | {vin}"
        )
    schedule_b_table = "\n".join(schedule_b_rows) if schedule_b_rows else "No vehicles listed"
    
    # Determine validity status
    if was_mte_compliant:
        validity_status = "Certificate is VALID immediately"
        validity_note = f"The operator met the Medium Term Exemption requirements on 1st May 2026."
    else:
        validity_status = "Certificate GRANTED but NOT VALID until minimum fleet proportion is achieved"
        validity_note = f"""⚠️ IMPORTANT VALIDITY CONDITION:

This certificate is GRANTED but NOT VALID for use until the operator achieves 
the minimum fleet proportion of {minimum_fleet_proportion:.1f}%.

On 1st May 2026, the operator had {in_scope_coaches} compliant coaches but was 
required to have {mte_minimum_coaches} compliant coaches under the Medium Term 
Exemption scheme.

This certificate CANNOT be used to provide home-to-school services using 
non-compliant vehicles until the operator achieves and maintains the minimum 
fleet proportion of {minimum_fleet_proportion:.1f}%.

The operator must notify the Department for Transport when they achieve this 
threshold to activate the certificate."""
    
    # Generate certificate text
    certificate = f"""
================================================================================
                    EQUALITY ACT 2010
         ORDER OF THE SECRETARY OF STATE UNDER SECTION 178
================================================================================

Operator:           {assessment_data.company_name}
O Licence:          {assessment_data.operator_licence_number}
Band:               {assessment_data.compliance_band}
Service Reference:  {service_reference}

================================================================================

The Secretary of State in exercise of the powers conferred by Section 178 of 
the Equality Act 2010, hereby authorises the use on roads of the regulated 
public service vehicles described in this Order notwithstanding that the 
vehicles do not comply with the requirements of Schedules 1 and 3 to the 
Public Service Vehicles Accessibility Regulations 2000, as amended, and 
subject to the terms and conditions set out in this Special Authorisation.

This Special Authorisation is valid only when the terms and conditions 
included in this certificate are met.

This Special Authorisation remains the property of the Secretary of State 
and may be withdrawn at any time at the discretion of the Secretary of State.

Signed by the authority of the Secretary of State:

{issue_date_str}

Liz Wilson
Deputy Director
Accessibility, Coaches, Taxis and Community Transport Division

Issue Date: {issue_date_str}
Expiry Date: {expiry_date_str}

================================================================================
    PUBLIC SERVICE VEHICLES ACCESSIBILITY REGULATIONS 2000
         SPECIAL AUTHORISATION TERMS AND CONDITIONS OF USE
================================================================================

1. This Order exempts relevant vehicles from Schedules I and III of the Public
   Service Vehicles Accessibility Regulations 2000 (PSVAR) when they are 
   providing relevant services, and is valid only when all of the conditions 
   specified here are complied with.

2. A separate Special Authorisation is hereby ordered for each of the Relevant
   Vehicles identified.

3. A "relevant vehicle" is a vehicle listed in Schedule B to this Order, and 
   to which the Order applies.

4. A "relevant service" is a "closed door home-to-school service", defined as
   a service to provide home-to-school transport for school or Further 
   Education pupils, and which can be used only by:
   a. a person receiving primary, secondary or further education or training 
      at an educational establishment served by the service;
   b. a person supervising or escorting any such person while they are using 
      such transport; or
   c. a person involved with the provision of education or training at that 
      establishment.

5. A copy of the front page of this Order must be carried aboard any relevant
   vehicle when it is providing a relevant service, and must be shown to a 
   Police Officer, or a person acting on behalf of the Driver and Vehicle 
   Standards Agency (DVSA) or Traffic Commissioner, upon request.

6. The operator must not provide any service within scope of PSVAR using a 
   Relevant Vehicle unless the service is a Relevant Service.

7. The Order will remain valid until its expiry date unless:
   a. The Secretary of State withdraws the Order, which they may do at their 
      sole discretion; or
   b. The operator of a relevant vehicle fails to comply with any one of the 
      validity conditions.

8. The Validity Conditions are:

   a. Maintaining minimum fleet compliance:
      The operator must maintain a minimum proportion of PSVAR compliant 
      coaches within their overall coach fleet. The applicable minimum 
      proportion is {minimum_fleet_proportion:.1f}% and will be fixed for this 
      operator for the validity of Special Authorisations applied to their 
      coaches.

   b. Any relevant vehicles which are used on relevant services but which are
      not PSVAR compliant, must in any case be "Partially Compliant", meaning
      they comply with the terms of Schedule 3 (2) – (5) of PSVAR, except for
      the requirements specified at Schedule A of this Order.

   c. Providing fleet data to the Secretary of State:
      The Operator provides a full, accurate and timely response to any 
      request from the Department for Transport or the Driver and Vehicle 
      Standards Agency for data concerning their coach fleet.

   d. New vehicle PSVAR enablement requirement:
      Any service operated by the Operator must be operated using a "PSVAR 
      enabled" vehicle where the vehicle operating that service is a coach 
      designed to carry more than twenty two passengers and first registered 
      on or after 1st February 2027.

   e. Fulfilment of requests for PSVAR compliant vehicles:
      Upon receipt of a valid request the Operator will arrange for an 
      available coach compliant with PSVAR to be provided.

   f. Operators must not charge or propose to charge more to provide a PSVAR
      compliant vehicle than they would to provide a non-compliant vehicle.

9. The operator obtains from the commissioner of Relevant Services confirmation
   that alternative accessible services will be provided for passengers who 
   cannot use a Relevant Service because it is provided using a Relevant 
   Vehicle.

10. This Order supersedes any Orders previously issued in relation to Relevant
    Vehicles.

11. The failure by the operator of a Relevant Vehicle to comply with these 
    terms will render any Special Authorisation applicable to the vehicles 
    they operate invalid, and leave the operator subject to enforcement action.

================================================================================
                    SCHEDULE A: MINIMUM FLEET PROPORTION
================================================================================

The Minimum fleet proportion of {minimum_fleet_proportion:.1f}% has been calculated as the 
higher of:

1. The combined total of PSVAR compliant coaches operated on home to school
   and rail replacement services, as a proportion of the total coach fleet; or

2. The combined total of PSVAR compliant coaches which the operator was, or
   would have been, required to operate on home to school and rail replacement
   services by the terms of the original Medium Term Exemption scheme, as a
   proportion of the total coach fleet.

CALCULATION DETAILS:
- In-scope compliant coaches on 1st May 2026: {in_scope_coaches}
- Total coaches on 1st May 2026: {all_coaches}
- Actual proportion: {actual_proportion:.1f}%
- MTE minimum requirement: {mte_minimum_coaches} coaches
- MTE minimum proportion: {mte_minimum_proportion:.1f}%
- Selected proportion: {minimum_fleet_proportion:.1f}% (the higher value)

{validity_note}

This proportion is fixed for the validity of this Special Authorisation.

================================================================================
                    SCHEDULE B: LIST OF RELEVANT VEHICLES
================================================================================

This Order grants Special Authorisations for the following vehicles:

Operator Name | Operator Licence Number | Vehicle Registration | Vehicle Chassis Number
{schedule_b_table}

================================================================================
                              END OF CERTIFICATE
================================================================================

IMPORTANT NOTES:

1. This certificate must be carried onboard each relevant vehicle when 
   providing relevant services.

2. The operator must maintain the minimum fleet proportion of {minimum_fleet_proportion:.1f}% 
   PSVAR compliant coaches across their entire coach fleet.

3. Alternative accessible transport must be available for passengers who 
   cannot use non-compliant vehicles.

4. This certificate is valid until {expiry_date_str} unless withdrawn by the 
   Secretary of State or the operator fails to comply with the validity 
   conditions.

5. Any relevant vehicles used on relevant services must be at least 
   "Partially Compliant" with PSVAR Schedule 3 (2)-(5).

6. New vehicles registered on or after 1st February 2027 must be "PSVAR 
   enabled" as defined in the validity conditions.

================================================================================

OPERATOR CONTACT INFORMATION:
Contact Name: {assessment_data.authorised_contact_name or 'Not provided'}
Contact Email: {assessment_data.authorised_contact_email or 'Not provided'}
Address: {assessment_data.authorised_contact_postal_address or 'Not provided'}
Postcode: {assessment_data.authorised_contact_postcode or 'Not provided'}

================================================================================
"""
    
    # Generate summary
    summary = (
        f"PSVAR exemption certificate generated for {assessment_data.company_name} "
        f"(Service Reference: {service_reference}). "
        f"Valid from {issue_date_str} to {expiry_date_str}. "
        f"Covers {len(all_vins)} vehicles with minimum fleet proportion of {minimum_fleet_proportion:.1f}%. "
        f"Band {assessment_data.compliance_band}. {validity_status}."
    )
    
    return CertificateGenerationOutput(
        success=True,
        certificate_text=certificate.strip(),
        certificate_summary=summary,
        service_reference=service_reference,
        minimum_fleet_proportion=minimum_fleet_proportion,
        is_valid_immediately=was_mte_compliant,
        validity_status=validity_status,
        issue_date=issue_date_str,
        expiry_date=expiry_date_str,
        vehicle_count=len(all_vins),
        band=assessment_data.compliance_band,
        calculation_details={
            "in_scope_compliant_coaches_may_2026": in_scope_coaches,
            "all_coaches_may_2026": all_coaches,
            "actual_proportion": round(actual_proportion, 1),
            "mte_minimum_coaches": mte_minimum_coaches,
            "mte_minimum_proportion": round(mte_minimum_proportion, 1),
            "was_mte_compliant": was_mte_compliant
        }
    )


# Made with Bob