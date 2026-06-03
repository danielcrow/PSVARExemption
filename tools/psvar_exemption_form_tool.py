from datetime import date
from math import ceil
from typing import Literal, Optional

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


# Type definitions
DecisionType = Literal[
    "OUT_OF_SCOPE",
    "EXEMPTION_NOT_NEEDED",
    "POTENTIALLY_EXEMPT_IF_VALID_CERTIFICATE_EXISTS",
    "NOT_EXEMPT",
    "EXEMPT_BUT_NON_COMPLIANT_WITH_CONDITIONS",
]

FinalCaseOutcome = Literal[
    "CAN_HAVE_EXEMPTION",
    "CANNOT_HAVE_EXEMPTION",
    "FURTHER_INVESTIGATION_REQUIRED",
    "OUT_OF_SCOPE",
    "EXEMPTION_NOT_REQUIRED",
]


# Input/Output schemas
class PSVARAssessmentInput(BaseModel):
    company_name: str = Field(description="Legal or trading name of the operator.")
    operator_licence_number: Optional[str] = Field(
        default=None,
        description="Operator licence number used for identification in the application.",
    )
    authorised_contact_name: Optional[str] = Field(
        default=None,
        description="Authorised contact name for the application.",
    )
    authorised_contact_telephone: Optional[str] = Field(
        default=None,
        description="Authorised contact telephone number.",
    )
    authorised_contact_email: Optional[str] = Field(
        default=None,
        description="Authorised contact email address.",
    )
    authorised_contact_postal_address: Optional[str] = Field(
        default=None,
        description="Authorised contact postal address for correspondence or certificate delivery.",
    )
    authorised_contact_postcode: Optional[str] = Field(
        default=None,
        description="Authorised contact postcode.",
    )
    service_types: list[str] = Field(
        description="Relevant service types operated. This HTS-only workflow expects HTS."
    )
    hts_closed_door: Optional[bool] = Field(
        default=None,
        description="Whether home-to-school services are closed-door services.",
    )
    hts_has_paying_customers: Optional[bool] = Field(
        default=None,
        description="Whether home-to-school services have paying customers.",
    )
    rr_when_train_unavailable: Optional[bool] = Field(
        default=None,
        description="Unused in this HTS-only workflow. Retained only for backward compatibility.",
    )
    total_hts_rr_fleet_size: int = Field(
        description="Total number of vehicles used for home-to-school services."
    )
    fully_compliant_vehicle_count: int = Field(
        description="Number of fully PSVAR compliant vehicles in the HTS fleet."
    )
    partially_compliant_vehicle_count: int = Field(
        description="Number of partially compliant vehicles in the HTS fleet."
    )
    non_compliant_vehicle_count: int = Field(
        description="Number of non-compliant vehicles in the HTS fleet."
    )
    temporarily_out_of_service_count: int = Field(
        default=0,
        description="Number of HTS fleet vehicles temporarily out of service.",
    )
    vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for each vehicle in the HTS fleet.",
    )
    partially_compliant_vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for the partially compliant vehicles in the HTS fleet.",
    )
    non_compliant_vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for the non-compliant vehicles in the HTS fleet.",
    )
    exemption_certificate_exists: bool = Field(
        description="Whether the operator holds an exemption certificate."
    )
    exemption_start_date: Optional[str] = Field(
        default=None,
        description="Exemption start date in ISO format YYYY-MM-DD.",
    )
    exemption_end_date: Optional[str] = Field(
        default=None,
        description="Exemption end date in ISO format YYYY-MM-DD.",
    )
    exemption_certificate_reference: Optional[str] = Field(
        default=None,
        description="Reference number or identifier for the exemption certificate.",
    )
    rail_commissioning_company_details: Optional[str] = Field(
        default=None,
        description="Unused in this HTS-only workflow. Retained only for backward compatibility.",
    )
    exemption_copy_carried_onboard: Optional[bool] = Field(
        default=None,
        description="Whether a copy of the exemption is carried onboard each relevant vehicle.",
    )
    alternative_accessible_transport_available: Optional[bool] = Field(
        default=None,
        description="Whether alternative accessible transport is available when needed.",
    )
    written_confirmation_retained: Optional[bool] = Field(
        default=None,
        description="Whether written confirmation of alternative accessible transport is retained.",
    )
    has_read_band_compliance_requirements: Optional[bool] = Field(
        default=None,
        description="Whether the operator confirms they have read their band compliance requirements.",
    )
    fleet_size_changed: Optional[bool] = Field(
        default=None,
        description="Whether the HTS fleet size has changed since exemption grant.",
    )
    dft_notified_within_5_days: Optional[bool] = Field(
        default=None,
        description="Whether DfT was notified within 5 working days of a band-changing fleet change.",
    )
    assessment_date: str = Field(
        description="Date of assessment in ISO format YYYY-MM-DD."
    )


class DVSATaskPayload(BaseModel):
    create_task: bool = Field(description="Whether a DVSA officer task should be created.")
    task_type: str = Field(description="Task type for DVSA workflow routing.")
    assigned_team: str = Field(description="Team responsible for manual review.")
    subject: str = Field(description="Short task subject.")
    description: str = Field(description="Detailed task description.")
    priority: str = Field(description="Task priority.")
    operator_company_name: str = Field(description="Operator company name.")
    operator_licence_number: Optional[str] = Field(
        default=None,
        description="Operator licence number.",
    )
    authorised_contact_name: Optional[str] = Field(
        default=None,
        description="Authorised contact name.",
    )
    authorised_contact_email: Optional[str] = Field(
        default=None,
        description="Authorised contact email.",
    )


class EmailNotificationPayload(BaseModel):
    send_email: bool = Field(description="Whether an outcome email should be sent.")
    to: str = Field(description="Recipient email address.")
    subject: str = Field(description="Email subject.")
    body: str = Field(description="Email body.")
    outcome: FinalCaseOutcome = Field(description="Final case outcome reflected in the email.")


class PSVARAssessmentOutput(BaseModel):
    decision: DecisionType = Field(description="Overall decision outcome.")
    final_case_outcome: FinalCaseOutcome = Field(
        description="Final triage outcome for exemption handling."
    )
    in_scope: bool = Field(description="Whether the service is in scope of this guidance.")
    exemption_needed: bool = Field(description="Whether an exemption is needed.")
    valid_exemption_certificate: bool = Field(
        description="Whether a valid exemption certificate appears to exist."
    )
    compliance_band: Optional[str] = Field(
        default=None,
        description="Compliance band A, B, C, or D if applicable.",
    )
    milestone_compliant: Optional[bool] = Field(
        default=None,
        description="Whether the operator meets the current milestone requirements.",
    )
    operational_conditions_compliant: Optional[bool] = Field(
        default=None,
        description="Whether operational exemption conditions appear to be met.",
    )
    dvsa_task_payload: DVSATaskPayload = Field(
        description="Payload describing whether a DVSA task should be created."
    )
    email_notification_payload: EmailNotificationPayload = Field(
        description="Payload describing the outcome email to send."
    )
    rationale: list[str] = Field(description="Reasons supporting the decision.")
    next_actions: list[str] = Field(description="Recommended next actions.")
    missing_information: list[str] = Field(
        description="Information still needed for a more certain assessment."
    )


@tool(
    permission=ToolPermission.READ_ONLY,
    display_name="PSVAR Exemption Assessment Form",
    description="Interactive form to collect operator information and assess PSVAR exemption eligibility for home-to-school transport services.",
)
def psvar_exemption_form_tool(
    # Section 1: Operator Information
    company_name: str = Field(description="Legal or trading name of the operator"),
    operator_licence_number: Optional[str] = Field(
        default=None,
        description="Operator licence number",
    ),
    authorised_contact_name: Optional[str] = Field(
        default=None,
        description="Authorised contact name",
    ),
    authorised_contact_telephone: Optional[str] = Field(
        default=None,
        description="Contact telephone number",
    ),
    authorised_contact_email: Optional[str] = Field(
        default=None,
        description="Contact email address",
    ),
    authorised_contact_postal_address: Optional[str] = Field(
        default=None,
        description="Postal address",
    ),
    authorised_contact_postcode: Optional[str] = Field(
        default=None,
        description="Postcode",
    ),
    
    # Section 2: Service Information
    service_types: list[str] = Field(
        default=["HTS"],
        description="Service types operated (HTS = Home-to-School, RR = Rail Replacement)",
    ),
    hts_closed_door: Optional[bool] = Field(
        default=None,
        description="Are HTS services closed-door? (pre-booked, not available to general public)",
    ),
    hts_has_paying_customers: Optional[bool] = Field(
        default=None,
        description="Do HTS services have paying customers?",
    ),
    
    # Section 3: Fleet Information
    total_hts_rr_fleet_size: int = Field(
        description="Total number of vehicles in HTS fleet",
    ),
    fully_compliant_vehicle_count: int = Field(
        description="Number of fully PSVAR compliant vehicles",
    ),
    partially_compliant_vehicle_count: int = Field(
        description="Number of partially compliant vehicles",
    ),
    non_compliant_vehicle_count: int = Field(
        description="Number of non-compliant vehicles",
    ),
    temporarily_out_of_service_count: int = Field(
        default=0,
        description="Number of vehicles temporarily out of service",
    ),
    
    # Section 4: Vehicle Identification Numbers
    vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for all vehicles (17 characters each)",
    ),
    partially_compliant_vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for partially compliant vehicles",
    ),
    non_compliant_vehicle_identification_numbers: list[str] = Field(
        default_factory=list,
        description="VINs for non-compliant vehicles",
    ),
    
    # Section 5: Exemption Certificate
    exemption_certificate_exists: bool = Field(
        description="Do you hold a PSVAR exemption certificate?",
    ),
    exemption_start_date: Optional[str] = Field(
        default=None,
        description="Exemption start date (YYYY-MM-DD)",
    ),
    exemption_end_date: Optional[str] = Field(
        default=None,
        description="Exemption end date (YYYY-MM-DD)",
    ),
    exemption_certificate_reference: Optional[str] = Field(
        default=None,
        description="Exemption certificate reference number",
    ),
    
    # Section 6: Operational Conditions
    exemption_copy_carried_onboard: Optional[bool] = Field(
        default=None,
        description="Is exemption copy carried onboard each relevant vehicle?",
    ),
    alternative_accessible_transport_available: Optional[bool] = Field(
        default=None,
        description="Is alternative accessible transport available when needed?",
    ),
    written_confirmation_retained: Optional[bool] = Field(
        default=None,
        description="Is written confirmation of alternative transport retained?",
    ),
    has_read_band_compliance_requirements: Optional[bool] = Field(
        default=None,
        description="Have you read and understood your band compliance requirements?",
    ),
    
    # Section 7: Fleet Changes
    fleet_size_changed: Optional[bool] = Field(
        default=None,
        description="Has fleet size changed since exemption grant?",
    ),
    dft_notified_within_5_days: Optional[bool] = Field(
        default=None,
        description="If fleet changed, was DfT notified within 5 working days?",
    ),
) -> dict:
    """
    PSVAR Exemption Assessment Form Tool
    
    This tool presents a form to collect all required information for assessing
    PSVAR exemption eligibility for home-to-school transport services, then
    evaluates the eligibility using deterministic rules.
    
    The form collects information across 7 sections:
    1. Operator Information
    2. Service Information
    3. Fleet Information
    4. Vehicle Identification Numbers
    5. Exemption Certificate Details
    6. Operational Conditions
    7. Fleet Changes
    
    Returns a comprehensive assessment with decision, rationale, and next actions.
    """
    
    # Import the evaluation function here to avoid module-level import issues
    import sys
    import os
    
    # Add parent directory to path to allow importing evaluate_psvar_exemption
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    from tools.evaluate_psvar_exemption import evaluate_psvar_exemption
    
    # Build the assessment input from form data
    assessment_input = PSVARAssessmentInput(
        company_name=company_name,
        operator_licence_number=operator_licence_number,
        authorised_contact_name=authorised_contact_name,
        authorised_contact_telephone=authorised_contact_telephone,
        authorised_contact_email=authorised_contact_email,
        authorised_contact_postal_address=authorised_contact_postal_address,
        authorised_contact_postcode=authorised_contact_postcode,
        service_types=service_types,
        hts_closed_door=hts_closed_door,
        hts_has_paying_customers=hts_has_paying_customers,
        rr_when_train_unavailable=None,
        total_hts_rr_fleet_size=total_hts_rr_fleet_size,
        fully_compliant_vehicle_count=fully_compliant_vehicle_count,
        partially_compliant_vehicle_count=partially_compliant_vehicle_count,
        non_compliant_vehicle_count=non_compliant_vehicle_count,
        temporarily_out_of_service_count=temporarily_out_of_service_count,
        vehicle_identification_numbers=vehicle_identification_numbers,
        partially_compliant_vehicle_identification_numbers=partially_compliant_vehicle_identification_numbers,
        non_compliant_vehicle_identification_numbers=non_compliant_vehicle_identification_numbers,
        exemption_certificate_exists=exemption_certificate_exists,
        exemption_start_date=exemption_start_date,
        exemption_end_date=exemption_end_date,
        exemption_certificate_reference=exemption_certificate_reference,
        rail_commissioning_company_details=None,
        exemption_copy_carried_onboard=exemption_copy_carried_onboard,
        alternative_accessible_transport_available=alternative_accessible_transport_available,
        written_confirmation_retained=written_confirmation_retained,
        has_read_band_compliance_requirements=has_read_band_compliance_requirements,
        fleet_size_changed=fleet_size_changed,
        dft_notified_within_5_days=dft_notified_within_5_days,
        assessment_date=date.today().isoformat(),
    )
    
    # Evaluate using the assessment tool
    result = evaluate_psvar_exemption(assessment_input)
    
    # Return the result (framework handles serialization)
    return result


# Made with Bob