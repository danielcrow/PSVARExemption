"""
Tool to generate PSVAR exemption certificates.
Creates the official exemption certificate document including Schedule B vehicle list.
"""

from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class VehicleEntry(BaseModel):
    """Single vehicle entry for Schedule B"""
    registration: str = Field(description="Vehicle registration number")
    vin: str = Field(description="Vehicle Identification Number (VIN/Chassis Number)")


class CertificateData(BaseModel):
    """Data required to generate exemption certificate"""
    operator_name: str = Field(description="Operator/company name")
    operator_licence_number: str = Field(description="Operator licence number")
    service_reference: str = Field(description="Service reference identifier")
    vehicles: list[VehicleEntry] = Field(description="List of vehicles for Schedule B")
    minimum_fleet_proportion: float = Field(description="Minimum fleet proportion percentage")
    band: str = Field(description="Compliance band (A, B, C, or D)")
    issue_date: str | None = Field(description="Certificate issue date (YYYY-MM-DD)", default=None)
    expiry_date: str | None = Field(description="Certificate expiry date (YYYY-MM-DD)", default=None)


class CertificateOutput(BaseModel):
    """Output from certificate generation"""
    success: bool = Field(description="Whether generation was successful")
    certificate_text: str = Field(description="Generated certificate text")
    message: str = Field(description="Confirmation message")


@tool(permission=ToolPermission.READ_ONLY)
def generate_exemption_certificate(certificate_data: CertificateData) -> CertificateOutput:
    """
    Generate a PSVAR exemption certificate document.
    
    Creates the official exemption certificate including:
    - Front page with operator details and validity dates
    - Terms and conditions (Schedules 1-3)
    - Schedule A calculation details
    - Schedule B vehicle list
    
    Args:
        certificate_data: All data required to generate the certificate
    
    Returns:
        CertificateOutput with success status and generated certificate text
    """
    
    # Set default dates if not provided
    issue_date = certificate_data.issue_date or datetime.now().strftime("%d/%m/%Y")
    # Default expiry: 2 years from issue
    if certificate_data.expiry_date:
        expiry_date = certificate_data.expiry_date
    else:
        expiry_dt = datetime.now() + timedelta(days=730)  # 2 years
        expiry_date = expiry_dt.strftime("%d/%m/%Y")
    
    # Generate Schedule B vehicle table
    schedule_b_rows = []
    for vehicle in certificate_data.vehicles:
        schedule_b_rows.append(
            f"{certificate_data.operator_name} | {certificate_data.operator_licence_number} | "
            f"{vehicle.registration} | {vehicle.vin}"
        )
    schedule_b_table = "\n".join(schedule_b_rows)
    
    # Generate certificate text
    certificate = f"""
================================================================================
                    EQUALITY ACT 2010
         ORDER OF THE SECRETARY OF STATE UNDER SECTION 178
================================================================================

Operator:           {certificate_data.operator_name}
O Licence:          {certificate_data.operator_licence_number}
Band:               {certificate_data.band}
Service Reference:  {certificate_data.service_reference}

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

{issue_date}

Liz Wilson
Deputy Director
Accessibility, Coaches, Taxis and Community Transport Division

Issue Date: {issue_date}
Expiry Date: {expiry_date}

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
      proportion is {certificate_data.minimum_fleet_proportion:.1f}% and will be fixed for this 
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

The Minimum fleet proportion of {certificate_data.minimum_fleet_proportion:.1f}% has been calculated as the 
higher of:

1. The combined total of PSVAR compliant coaches operated on home to school
   and rail replacement services, as a proportion of the total coach fleet; or

2. The combined total of PSVAR compliant coaches which the operator was, or
   would have been, required to operate on home to school and rail replacement
   services by the terms of the original Medium Term Exemption scheme, as a
   proportion of the total coach fleet.

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

2. The operator must maintain the minimum fleet proportion of {certificate_data.minimum_fleet_proportion:.1f}% 
   PSVAR compliant coaches across their entire coach fleet.

3. Alternative accessible transport must be available for passengers who 
   cannot use non-compliant vehicles.

4. This certificate is valid until {expiry_date} unless withdrawn by the 
   Secretary of State or the operator fails to comply with the validity 
   conditions.

================================================================================
"""
    
    return CertificateOutput(
        success=True,
        certificate_text=certificate.strip(),
        message=f"✓ Exemption certificate generated successfully for {certificate_data.operator_name}. "
                f"Certificate valid from {issue_date} to {expiry_date}. "
                f"Covers {len(certificate_data.vehicles)} vehicles with minimum fleet proportion of {certificate_data.minimum_fleet_proportion:.1f}%."
    )

# Made with Bob