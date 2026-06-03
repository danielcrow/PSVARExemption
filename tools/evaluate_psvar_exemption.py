from datetime import date
from math import ceil
from typing import Literal, Optional

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool


VIN_TRANSLITERATION = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "J": 1,
    "K": 2,
    "L": 3,
    "M": 4,
    "N": 5,
    "P": 7,
    "R": 9,
    "S": 2,
    "T": 3,
    "U": 4,
    "V": 5,
    "W": 6,
    "X": 7,
    "Y": 8,
    "Z": 9,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}

VIN_POSITION_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
INVALID_VIN_CHARACTERS = {"I", "O", "Q"}


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


def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    return date.fromisoformat(value)


def _normalize_vin(vin: str) -> str:
    return vin.strip().upper()


def _calculate_vin_check_digit(vin: str) -> str:
    total = 0
    for index, character in enumerate(vin):
        total += VIN_TRANSLITERATION[character] * VIN_POSITION_WEIGHTS[index]
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)


def _validate_vin(vin: str) -> list[str]:
    errors: list[str] = []
    normalized_vin = _normalize_vin(vin)

    if len(normalized_vin) != 17:
        errors.append("must be exactly 17 characters long")
        return errors

    invalid_characters = [
        character
        for character in normalized_vin
        if character not in VIN_TRANSLITERATION or character in INVALID_VIN_CHARACTERS
    ]
    if invalid_characters:
        errors.append(
            "contains invalid characters; VINs may only use digits and uppercase letters excluding I, O, and Q"
        )
        return errors

    expected_check_digit = _calculate_vin_check_digit(normalized_vin)
    actual_check_digit = normalized_vin[8]
    if actual_check_digit != expected_check_digit:
        errors.append(
            f"has an invalid check digit; expected {expected_check_digit} in position 9"
        )

    return errors


def _collect_vin_validation_issues(
    vins: list[str],
    label: str,
) -> tuple[list[str], list[str]]:
    rationale: list[str] = []
    missing_information: list[str] = []

    normalized_vins = [_normalize_vin(vin) for vin in vins if vin and vin.strip()]
    duplicates = sorted({vin for vin in normalized_vins if normalized_vins.count(vin) > 1})
    if duplicates:
        rationale.append(
            f"Duplicate VINs were provided in {label}: {', '.join(duplicates)}."
        )
        missing_information.append(
            f"Provide unique valid VINs for {label}; duplicate VINs are not allowed."
        )

    for vin in normalized_vins:
        vin_errors = _validate_vin(vin)
        if vin_errors:
            rationale.append(f"VIN {vin} in {label} " + "; ".join(vin_errors) + ".")
            missing_information.append(
                f"Correct or replace invalid VIN {vin} in {label}."
            )

    return rationale, missing_information


def _determine_band(fleet_size: int) -> Optional[str]:
    if fleet_size <= 0:
        return None
    if 1 <= fleet_size <= 5:
        return "A"
    if 6 <= fleet_size <= 9:
        return "B"
    if 10 <= fleet_size <= 29:
        return "C"
    return "D"


def _required_counts_for_date(band: str, fleet_size: int, as_of: date) -> dict:
    requirements = {
        "minimum_fully_compliant": 0,
        "minimum_partially_compliant": 0,
        "remaining_must_be_partially_compliant": False,
    }

    if as_of < date(2023, 8, 1):
        return requirements

    if band == "A":
        if as_of < date(2024, 8, 1):
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.25)
        elif as_of < date(2025, 8, 1):
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.50)
        else:
            requirements["minimum_fully_compliant"] = 1
            requirements["remaining_must_be_partially_compliant"] = True

    elif band == "B":
        if as_of < date(2024, 8, 1):
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.25)
        elif as_of < date(2025, 8, 1):
            requirements["minimum_fully_compliant"] = 1
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.50)
        else:
            requirements["minimum_fully_compliant"] = 2
            requirements["remaining_must_be_partially_compliant"] = True

    elif band == "C":
        if as_of < date(2024, 8, 1):
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.25)
        elif as_of < date(2025, 8, 1):
            requirements["minimum_fully_compliant"] = ceil(fleet_size * 0.15)
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.50)
        else:
            requirements["minimum_fully_compliant"] = ceil(fleet_size * 0.25)
            requirements["remaining_must_be_partially_compliant"] = True

    elif band == "D":
        if as_of < date(2024, 8, 1):
            requirements["minimum_fully_compliant"] = ceil(fleet_size * 0.15)
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.25)
        elif as_of < date(2025, 8, 1):
            requirements["minimum_fully_compliant"] = ceil(fleet_size * 0.25)
            requirements["minimum_partially_compliant"] = ceil(fleet_size * 0.50)
        else:
            requirements["minimum_fully_compliant"] = ceil(fleet_size * 0.35)
            requirements["remaining_must_be_partially_compliant"] = True

    return requirements


def _evaluate_milestone(
    band: str,
    fleet_size: int,
    fully_compliant: int,
    partially_compliant: int,
    non_compliant: int,
    as_of: date,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    requirements = _required_counts_for_date(band, fleet_size, as_of)

    if requirements["minimum_fully_compliant"] > fully_compliant:
        reasons.append(
            f"Requires at least {requirements['minimum_fully_compliant']} fully compliant vehicles by {as_of.isoformat()} assessment date."
        )

    if requirements["minimum_partially_compliant"] > partially_compliant:
        reasons.append(
            f"Requires at least {requirements['minimum_partially_compliant']} partially compliant vehicles by {as_of.isoformat()} assessment date."
        )

    if requirements["remaining_must_be_partially_compliant"]:
        remaining = fleet_size - fully_compliant
        if partially_compliant < remaining or non_compliant > 0:
            reasons.append(
                "All remaining vehicles must be at least partially compliant at this stage."
            )

    return (len(reasons) == 0, reasons)


def _build_dvsa_task_payload(
    assessment: PSVARAssessmentInput,
    final_case_outcome: FinalCaseOutcome,
    rationale: list[str],
    missing_information: list[str],
) -> DVSATaskPayload:
    create_task = final_case_outcome == "FURTHER_INVESTIGATION_REQUIRED"
    description_lines = [
        f"Operator: {assessment.company_name}",
        f"Operator licence number: {assessment.operator_licence_number or 'Not provided'}",
        f"Assessment date: {assessment.assessment_date}",
        f"Final case outcome: {final_case_outcome}",
        "Rationale:",
        *[f"- {item}" for item in rationale],
    ]
    if missing_information:
        description_lines.extend(
            ["Missing information:", *[f"- {item}" for item in missing_information]]
        )

    return DVSATaskPayload(
        create_task=create_task,
        task_type="PSVAR_HTS_EXEMPTION_REVIEW",
        assigned_team="DVSA Officer",
        subject=f"PSVAR HTS exemption review for {assessment.company_name}",
        description="\n".join(description_lines),
        priority="High" if create_task else "Normal",
        operator_company_name=assessment.company_name,
        operator_licence_number=assessment.operator_licence_number,
        authorised_contact_name=assessment.authorised_contact_name,
        authorised_contact_email=assessment.authorised_contact_email,
    )


def _build_email_notification_payload(
    assessment: PSVARAssessmentInput,
    final_case_outcome: FinalCaseOutcome,
    rationale: list[str],
    next_actions: list[str],
) -> EmailNotificationPayload:
    outcome_titles = {
        "CAN_HAVE_EXEMPTION": "PSVAR HTS exemption outcome: eligible",
        "CANNOT_HAVE_EXEMPTION": "PSVAR HTS exemption outcome: not eligible",
        "FURTHER_INVESTIGATION_REQUIRED": "PSVAR HTS exemption outcome: further investigation required",
        "OUT_OF_SCOPE": "PSVAR HTS exemption outcome: out of scope",
        "EXEMPTION_NOT_REQUIRED": "PSVAR HTS exemption outcome: exemption not required",
    }
    subject = outcome_titles[final_case_outcome]
    body_lines = [
        f"Dear {assessment.authorised_contact_name or assessment.company_name},",
        "",
        f"The outcome of your PSVAR HTS exemption assessment is: {final_case_outcome}.",
        "",
        "Rationale:",
        *[f"- {item}" for item in rationale],
    ]
    if next_actions:
        body_lines.extend(["", "Next actions:", *[f"- {item}" for item in next_actions]])

    return EmailNotificationPayload(
        send_email=bool(assessment.authorised_contact_email),
        to=assessment.authorised_contact_email or "",
        subject=subject,
        body="\n".join(body_lines),
        outcome=final_case_outcome,
    )


@tool(permission=ToolPermission.READ_ONLY)
def evaluate_psvar_exemption(
    assessment: PSVARAssessmentInput,
) -> PSVARAssessmentOutput:
    """
    Evaluate whether an operator can rely on the PSVAR exemption guidance for
    home-to-school services in this HTS-only workflow.
    """
    rationale: list[str] = []
    next_actions: list[str] = []
    missing_information: list[str] = []

    if not assessment.operator_licence_number:
        missing_information.append("Operator licence number.")
    if not assessment.authorised_contact_name:
        missing_information.append("Authorised contact name.")
    if not assessment.authorised_contact_telephone:
        missing_information.append("Authorised contact telephone number.")
    if not assessment.authorised_contact_email:
        missing_information.append("Authorised contact email address.")
    if not assessment.authorised_contact_postal_address:
        missing_information.append("Authorised contact postal address.")
    if not assessment.authorised_contact_postcode:
        missing_information.append("Authorised contact postcode.")
    if assessment.has_read_band_compliance_requirements is None:
        missing_information.append(
            "Confirmation that the operator has read their band compliance requirements."
        )

    service_types = {service.upper() for service in assessment.service_types}
    assessment_date = _parse_iso_date(assessment.assessment_date)

    if assessment_date is None:
        raise ValueError("assessment_date must be provided in ISO format YYYY-MM-DD.")

    if "HTS" not in service_types:
        rationale = ["Operator does not provide eligible home-to-school services for this HTS-only workflow."]
        next_actions = []
        missing_information = []
        final_case_outcome = "OUT_OF_SCOPE"
        return PSVARAssessmentOutput(
            decision="OUT_OF_SCOPE",
            final_case_outcome=final_case_outcome,
            in_scope=False,
            exemption_needed=False,
            valid_exemption_certificate=False,
            dvsa_task_payload=_build_dvsa_task_payload(
                assessment, final_case_outcome, rationale, missing_information
            ),
            email_notification_payload=_build_email_notification_payload(
                assessment, final_case_outcome, rationale, next_actions
            ),
            rationale=rationale,
            next_actions=next_actions,
            missing_information=missing_information,
        )

    if "HTS" in service_types:
        if assessment.hts_closed_door is None:
            missing_information.append("Whether HTS services are closed-door.")
        elif assessment.hts_closed_door is False:
            rationale.append("HTS services are not closed-door and are outside this exemption guidance.")
            final_case_outcome = "OUT_OF_SCOPE"
            return PSVARAssessmentOutput(
                decision="OUT_OF_SCOPE",
                final_case_outcome=final_case_outcome,
                in_scope=False,
                exemption_needed=False,
                valid_exemption_certificate=False,
                dvsa_task_payload=_build_dvsa_task_payload(
                    assessment, final_case_outcome, rationale, missing_information
                ),
                email_notification_payload=_build_email_notification_payload(
                    assessment, final_case_outcome, rationale, []
                ),
                rationale=rationale,
                next_actions=[],
                missing_information=missing_information,
            )

        if assessment.hts_has_paying_customers is None:
            missing_information.append("Whether HTS services have paying customers.")
        elif service_types == {"HTS"} and assessment.hts_has_paying_customers is False:
            rationale.append("HTS services with no paying customers are outside PSVAR scope.")
            final_case_outcome = "OUT_OF_SCOPE"
            return PSVARAssessmentOutput(
                decision="OUT_OF_SCOPE",
                final_case_outcome=final_case_outcome,
                in_scope=False,
                exemption_needed=False,
                valid_exemption_certificate=False,
                dvsa_task_payload=_build_dvsa_task_payload(
                    assessment, final_case_outcome, rationale, missing_information
                ),
                email_notification_payload=_build_email_notification_payload(
                    assessment, final_case_outcome, rationale, []
                ),
                rationale=rationale,
                next_actions=[],
                missing_information=missing_information,
            )

    if "RR" in service_types:
        rationale.append(
            "Rail replacement services are not assessed in this HTS-only workflow."
        )

    fleet_total_from_counts = (
        assessment.fully_compliant_vehicle_count
        + assessment.partially_compliant_vehicle_count
        + assessment.non_compliant_vehicle_count
    )

    if fleet_total_from_counts != assessment.total_hts_rr_fleet_size:
        rationale.append(
            "Fleet counts do not match the declared total HTS fleet size."
        )
        next_actions.append(
            "Reconcile fully compliant, partially compliant, and non-compliant vehicle counts."
        )

    if len(assessment.vehicle_identification_numbers) != assessment.total_hts_rr_fleet_size:
        missing_information.append(
            "Vehicle Identification Number (VIN) for each vehicle in the HTS fleet."
        )
    else:
        vin_rationale, vin_missing_information = _collect_vin_validation_issues(
            assessment.vehicle_identification_numbers,
            "the HTS fleet",
        )
        rationale.extend(vin_rationale)
        missing_information.extend(vin_missing_information)

    if (
        assessment.partially_compliant_vehicle_count > 0
        and len(assessment.partially_compliant_vehicle_identification_numbers)
        != assessment.partially_compliant_vehicle_count
    ):
        missing_information.append(
            "Vehicle Identification Number (VIN) for each partially compliant vehicle in the HTS fleet."
        )
    elif assessment.partially_compliant_vehicle_count > 0:
        partial_vin_rationale, partial_vin_missing_information = _collect_vin_validation_issues(
            assessment.partially_compliant_vehicle_identification_numbers,
            "the partially compliant HTS vehicles",
        )
        rationale.extend(partial_vin_rationale)
        missing_information.extend(partial_vin_missing_information)

    if (
        assessment.non_compliant_vehicle_count > 0
        and len(assessment.non_compliant_vehicle_identification_numbers)
        != assessment.non_compliant_vehicle_count
    ):
        missing_information.append(
            "Vehicle Identification Number (VIN) for each non-compliant vehicle in the HTS fleet."
        )
    elif assessment.non_compliant_vehicle_count > 0:
        non_compliant_vin_rationale, non_compliant_vin_missing_information = _collect_vin_validation_issues(
            assessment.non_compliant_vehicle_identification_numbers,
            "the non-compliant HTS vehicles",
        )
        rationale.extend(non_compliant_vin_rationale)
        missing_information.extend(non_compliant_vin_missing_information)

    if assessment.total_hts_rr_fleet_size <= 0:
        rationale = ["No HTS fleet vehicles were identified."]
        next_actions = []
        final_case_outcome = "OUT_OF_SCOPE"
        return PSVARAssessmentOutput(
            decision="OUT_OF_SCOPE",
            final_case_outcome=final_case_outcome,
            in_scope=False,
            exemption_needed=False,
            valid_exemption_certificate=False,
            dvsa_task_payload=_build_dvsa_task_payload(
                assessment, final_case_outcome, rationale, missing_information
            ),
            email_notification_payload=_build_email_notification_payload(
                assessment, final_case_outcome, rationale, next_actions
            ),
            rationale=rationale,
            next_actions=next_actions,
            missing_information=missing_information,
        )

    if (
        assessment.partially_compliant_vehicle_count == 0
        and assessment.non_compliant_vehicle_count == 0
    ):
        rationale.append("All relevant HTS vehicles are fully PSVAR compliant.")
        next_actions = ["Continue maintaining full PSVAR compliance across the fleet."]
        final_case_outcome = "EXEMPTION_NOT_REQUIRED"
        return PSVARAssessmentOutput(
            decision="EXEMPTION_NOT_NEEDED",
            final_case_outcome=final_case_outcome,
            in_scope=True,
            exemption_needed=False,
            valid_exemption_certificate=False,
            dvsa_task_payload=_build_dvsa_task_payload(
                assessment, final_case_outcome, rationale, missing_information
            ),
            email_notification_payload=_build_email_notification_payload(
                assessment, final_case_outcome, rationale, next_actions
            ),
            rationale=rationale,
            next_actions=next_actions,
            missing_information=missing_information,
        )

    exemption_needed = True

    band = _determine_band(assessment.total_hts_rr_fleet_size)
    milestone_compliant = None

    if band is not None:
        milestone_compliant, milestone_reasons = _evaluate_milestone(
            band=band,
            fleet_size=assessment.total_hts_rr_fleet_size,
            fully_compliant=assessment.fully_compliant_vehicle_count,
            partially_compliant=assessment.partially_compliant_vehicle_count,
            non_compliant=assessment.non_compliant_vehicle_count,
            as_of=assessment_date,
        )
        rationale.extend(milestone_reasons)

    # This is an APPLICATION assessment - operator is applying for a certificate
    if not assessment.exemption_certificate_exists:
        # Check if they meet milestone requirements
        if milestone_compliant is False:
            rationale.append(
                "The fleet does not currently meet the compliance milestone requirements for its band."
            )
            rationale.append(
                "To be eligible for an exemption certificate, you must first meet the minimum milestone requirements."
            )
            next_actions.append(
                "Increase the number of fully compliant and/or partially compliant vehicles to meet your band's milestone requirements."
            )
            next_actions.append(
                "Once you meet the milestone requirements, you can reapply for an exemption certificate."
            )
            final_case_outcome = (
                "FURTHER_INVESTIGATION_REQUIRED" if missing_information else "CANNOT_HAVE_EXEMPTION"
            )
            return PSVARAssessmentOutput(
                decision="NOT_EXEMPT",
                final_case_outcome=final_case_outcome,
                in_scope=True,
                exemption_needed=exemption_needed,
                valid_exemption_certificate=False,
                compliance_band=band,
                milestone_compliant=milestone_compliant,
                operational_conditions_compliant=None,
                dvsa_task_payload=_build_dvsa_task_payload(
                    assessment, final_case_outcome, rationale, missing_information
                ),
                email_notification_payload=_build_email_notification_payload(
                    assessment, final_case_outcome, rationale, next_actions
                ),
                rationale=rationale,
                next_actions=next_actions,
                missing_information=missing_information,
            )

        # Check operational plans for partially/non-compliant vehicles
        operational_plans_compliant = True
        
        if assessment.partially_compliant_vehicle_count > 0 or assessment.non_compliant_vehicle_count > 0:
            if assessment.exemption_copy_carried_onboard is None:
                missing_information.append(
                    "Confirmation that exemption copies will be carried onboard each relevant vehicle."
                )
            elif assessment.exemption_copy_carried_onboard is False:
                operational_plans_compliant = False
                rationale.append(
                    "You must commit to carrying exemption copies onboard each partially/non-compliant vehicle."
                )

            if assessment.alternative_accessible_transport_available is None:
                missing_information.append(
                    "Confirmation that alternative accessible transport will be available when needed."
                )
            elif assessment.alternative_accessible_transport_available is False:
                operational_plans_compliant = False
                rationale.append(
                    "You must commit to providing alternative accessible transport for passengers unable to access exempt vehicles."
                )

            if assessment.written_confirmation_retained is None:
                missing_information.append(
                    "Confirmation that written confirmation of alternative transport will be retained."
                )
            elif assessment.written_confirmation_retained is False:
                operational_plans_compliant = False
                rationale.append(
                    "You must commit to retaining written confirmation of alternative accessible transport arrangements."
                )

        if not operational_plans_compliant:
            next_actions.append(
                "Commit to meeting all operational conditions required for the exemption."
            )
            final_case_outcome = "CANNOT_HAVE_EXEMPTION"
            return PSVARAssessmentOutput(
                decision="NOT_EXEMPT",
                final_case_outcome=final_case_outcome,
                in_scope=True,
                exemption_needed=exemption_needed,
                valid_exemption_certificate=False,
                compliance_band=band,
                milestone_compliant=milestone_compliant,
                operational_conditions_compliant=operational_plans_compliant,
                dvsa_task_payload=_build_dvsa_task_payload(
                    assessment, final_case_outcome, rationale, missing_information
                ),
                email_notification_payload=_build_email_notification_payload(
                    assessment, final_case_outcome, rationale, next_actions
                ),
                rationale=rationale,
                next_actions=next_actions,
                missing_information=missing_information,
            )

        # Fleet meets milestones and operational plans are acceptable - ELIGIBLE!
        rationale.append(
            "The fleet meets the current band milestone requirements."
        )
        rationale.append(
            "Operational plans for alternative accessible transport are acceptable."
        )
        rationale.append(
            "You appear eligible for a PSVAR exemption certificate."
        )
        next_actions.append(
            "Submit your formal exemption certificate application to DfT."
        )
        next_actions.append(
            "Once granted, ensure you meet all ongoing milestone requirements and operational conditions."
        )
        next_actions.append(
            "Notify DfT within 5 working days of any fleet changes that affect your band."
        )
        final_case_outcome = "CAN_HAVE_EXEMPTION" if not missing_information else "FURTHER_INVESTIGATION_REQUIRED"
        return PSVARAssessmentOutput(
            decision="POTENTIALLY_EXEMPT_IF_VALID_CERTIFICATE_EXISTS",
            final_case_outcome=final_case_outcome,
            in_scope=True,
            exemption_needed=exemption_needed,
            valid_exemption_certificate=False,
            compliance_band=band,
            milestone_compliant=milestone_compliant,
            operational_conditions_compliant=operational_plans_compliant,
            dvsa_task_payload=_build_dvsa_task_payload(
                assessment, final_case_outcome, rationale, missing_information
            ),
            email_notification_payload=_build_email_notification_payload(
                assessment, final_case_outcome, rationale, next_actions
            ),
            rationale=rationale,
            next_actions=next_actions,
            missing_information=missing_information,
        )

    exemption_start = _parse_iso_date(assessment.exemption_start_date)
    exemption_end = _parse_iso_date(assessment.exemption_end_date)

    if exemption_start is None:
        missing_information.append("Exemption start date.")
    if exemption_end is None:
        missing_information.append("Exemption end date.")
    if not assessment.exemption_certificate_reference:
        missing_information.append("Exemption certificate reference.")

    valid_certificate = True
    if exemption_end and assessment_date > exemption_end:
        valid_certificate = False
        rationale.append("The exemption certificate appears to have expired.")
    if assessment_date > date(2026, 7, 31):
        valid_certificate = False
        rationale.append(
            "This exemption regime expired on 2026-07-31 and full PSVAR compliance is expected from 2026-08-01."
        )

    if not valid_certificate:
        next_actions.append(
            "Do not rely on the expired exemption; ensure full PSVAR compliance or obtain updated regulatory guidance."
        )
        final_case_outcome = "CANNOT_HAVE_EXEMPTION"
        return PSVARAssessmentOutput(
            decision="NOT_EXEMPT",
            final_case_outcome=final_case_outcome,
            in_scope=True,
            exemption_needed=exemption_needed,
            valid_exemption_certificate=False,
            dvsa_task_payload=_build_dvsa_task_payload(
                assessment, final_case_outcome, rationale, missing_information
            ),
            email_notification_payload=_build_email_notification_payload(
                assessment, final_case_outcome, rationale, next_actions
            ),
            rationale=rationale,
            next_actions=next_actions,
            missing_information=missing_information,
        )

    operational_conditions_compliant = True

    if assessment.exemption_copy_carried_onboard is None:
        missing_information.append(
            "Whether a copy of the exemption is carried onboard each relevant vehicle."
        )
    elif assessment.exemption_copy_carried_onboard is False:
        operational_conditions_compliant = False
        rationale.append(
            "A copy of the exemption must be carried onboard each relevant non-fully-compliant vehicle."
        )

    if assessment.alternative_accessible_transport_available is None:
        missing_information.append(
            "Whether alternative accessible transport is available when needed."
        )
    elif assessment.alternative_accessible_transport_available is False:
        operational_conditions_compliant = False
        rationale.append(
            "Alternative accessible transport must be available for passengers unable to access exempt vehicles."
        )

    if assessment.written_confirmation_retained is None:
        missing_information.append(
            "Whether written confirmation of alternative accessible transport is retained."
        )
    elif assessment.written_confirmation_retained is False:
        operational_conditions_compliant = False
        rationale.append(
            "Written confirmation of alternative accessible transport must be retained alongside the exemption."
        )

    band = _determine_band(assessment.total_hts_rr_fleet_size)
    milestone_compliant = None

    if band is not None:
        milestone_compliant, milestone_reasons = _evaluate_milestone(
            band=band,
            fleet_size=assessment.total_hts_rr_fleet_size,
            fully_compliant=assessment.fully_compliant_vehicle_count,
            partially_compliant=assessment.partially_compliant_vehicle_count,
            non_compliant=assessment.non_compliant_vehicle_count,
            as_of=assessment_date,
        )
        rationale.extend(milestone_reasons)

    if assessment.has_read_band_compliance_requirements is False:
        operational_conditions_compliant = False
        rationale.append(
            "The operator must confirm they have read their band compliance requirements."
        )

    if assessment.fleet_size_changed is None:
        missing_information.append("Whether the fleet size has changed since exemption grant.")
    elif assessment.fleet_size_changed:
        if assessment.dft_notified_within_5_days is None:
            missing_information.append(
                "Whether DfT was notified within 5 working days of the band-changing fleet change."
            )
        elif assessment.dft_notified_within_5_days is False:
            operational_conditions_compliant = False
            rationale.append(
                "Operators must notify DfT within 5 working days where a band change occurs."
            )

    if not operational_conditions_compliant or milestone_compliant is False:
        next_actions.append(
            "Address the failed exemption conditions and compliance milestones immediately."
        )
        next_actions.append("Review fleet banding and milestone thresholds.")
        final_case_outcome = "FURTHER_INVESTIGATION_REQUIRED"
        return PSVARAssessmentOutput(
            decision="EXEMPT_BUT_NON_COMPLIANT_WITH_CONDITIONS",
            final_case_outcome=final_case_outcome,
            in_scope=True,
            exemption_needed=exemption_needed,
            valid_exemption_certificate=True,
            compliance_band=band,
            milestone_compliant=milestone_compliant,
            operational_conditions_compliant=operational_conditions_compliant,
            dvsa_task_payload=_build_dvsa_task_payload(
                assessment, final_case_outcome, rationale, missing_information
            ),
            email_notification_payload=_build_email_notification_payload(
                assessment, final_case_outcome, rationale, next_actions
            ),
            rationale=rationale,
            next_actions=next_actions,
            missing_information=missing_information,
        )

    rationale.append(
        "The operator appears to have an in-scope service, a valid exemption certificate, and no identified breach of current exemption conditions."
    )
    next_actions.append(
        "Retain evidence supporting the exemption and continue monitoring milestone dates and fleet band changes."
    )

    final_case_outcome: FinalCaseOutcome = (
        "FURTHER_INVESTIGATION_REQUIRED" if missing_information else "CAN_HAVE_EXEMPTION"
    )
    return PSVARAssessmentOutput(
        decision="POTENTIALLY_EXEMPT_IF_VALID_CERTIFICATE_EXISTS",
        final_case_outcome=final_case_outcome,
        in_scope=True,
        exemption_needed=exemption_needed,
        valid_exemption_certificate=True,
        compliance_band=band,
        milestone_compliant=milestone_compliant,
        operational_conditions_compliant=operational_conditions_compliant,
        dvsa_task_payload=_build_dvsa_task_payload(
            assessment, final_case_outcome, rationale, missing_information
        ),
        email_notification_payload=_build_email_notification_payload(
            assessment, final_case_outcome, rationale, next_actions
        ),
        rationale=rationale,
        next_actions=next_actions,
        missing_information=missing_information,
    )

# Made with Bob
