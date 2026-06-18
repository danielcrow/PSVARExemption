"""
Flow to generate PSVAR exemption certificates using LLM prompt.
Integrates with watsonx Orchestrate to create official certificates from application data.
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END


class VehicleEntry(BaseModel):
    """Single vehicle entry for Schedule B"""
    registration: str = Field(description="Vehicle registration number (e.g., AB12 CDE)")
    vin: str = Field(description="Vehicle Identification Number - 17 characters (VIN/Chassis Number)")


class CalculationDetails(BaseModel):
    """Details of the Schedule A minimum fleet proportion calculation"""
    in_scope_compliant_coaches_may_2026: int = Field(
        description="Total number of fully PSVAR compliant coaches used on 1st May 2026 for HTS and RR services"
    )
    all_coaches_may_2026: int = Field(
        description="Total number of coaches in fleet on 1st May 2026 (all services)"
    )
    actual_proportion: float = Field(
        description="Actual proportion of compliant coaches as percentage"
    )
    mte_minimum_proportion: float = Field(
        description="MTE minimum requirement proportion as percentage"
    )
    was_mte_compliant: bool = Field(
        description="Whether operator met MTE requirements on 1st May 2026"
    )


class CertificateInput(BaseModel):
    """Input data for certificate generation"""
    operator_name: str = Field(description="Operator/company name")
    operator_licence_number: str = Field(description="Operator licence number (e.g., OD1234567)")
    service_reference: str = Field(description="Service reference identifier (e.g., PSVAR-2026-001)")
    band: str = Field(description="Compliance band: A, B, C, or D")
    minimum_fleet_proportion: float = Field(description="Minimum fleet proportion percentage (e.g., 20.0)")
    issue_date: str = Field(description="Certificate issue date in DD/MM/YYYY format")
    expiry_date: str = Field(description="Certificate expiry date in DD/MM/YYYY format")
    vehicles: list[VehicleEntry] = Field(description="List of vehicles for Schedule B")
    calculation_details: CalculationDetails = Field(description="Schedule A calculation details")


class CertificateOutput(BaseModel):
    """Output from certificate generation flow"""
    success: bool = Field(description="Whether certificate generation was successful")
    certificate_text: str = Field(description="Complete formatted certificate text")
    certificate_summary: str = Field(description="Brief summary of the certificate")
    operator_name: str = Field(description="Operator name from certificate")
    service_reference: str = Field(description="Service reference from certificate")
    minimum_fleet_proportion: float = Field(description="Minimum fleet proportion percentage")
    is_valid_immediately: bool = Field(description="Whether certificate is valid immediately or conditional")
    validity_status: str = Field(description="Certificate validity status message")
    issue_date: str = Field(description="Certificate issue date")
    expiry_date: str = Field(description="Certificate expiry date")
    vehicle_count: int = Field(description="Number of vehicles covered by certificate")
    band: str = Field(description="Compliance band")


@flow(
    name="generate_psvar_certificate",
    display_name="Generate PSVAR Exemption Certificate",
    description="Generate official PSVAR exemption certificate from application data using LLM",
    input_schema=CertificateInput
)
def build_generate_certificate_flow(aflow: Flow) -> Flow:
    """
    Flow to generate PSVAR exemption certificates.
    
    This flow:
    1. Takes certificate input data
    2. Constructs a detailed prompt for the LLM
    3. Generates the complete certificate text
    4. Formats the output with metadata
    
    Args:
        aflow: Flow builder instance
        
    Returns:
        Configured flow
    """
    
    # Create prompt node to generate certificate
    generate_cert = aflow.prompt(
        name="generate_certificate",
        system_prompt="""You are an official UK government document generator for the Department for Transport. 
You generate formal PSVAR exemption certificates under Section 178 of the Equality Act 2010.

Your certificates must:
- Follow official UK government legal document format
- Include all required sections and legal text
- Use formal, authoritative language
- Be precise and legally accurate
- Include proper formatting with section dividers (====)
- Follow the exact structure specified in the prompt""",
        user_prompt=["""Generate a complete, formal PSVAR exemption certificate using this data:

**OPERATOR INFORMATION:**
- Operator Name: {operator_name}
- Operator Licence Number: {operator_licence_number}
- Service Reference: {service_reference}
- Compliance Band: {band}

**CERTIFICATE DETAILS:**
- Issue Date: {issue_date}
- Expiry Date: {expiry_date}
- Minimum Fleet Proportion: {minimum_fleet_proportion}%

**VEHICLES (Schedule B):**
{vehicles_list}

**CALCULATION DETAILS (Schedule A):**
- In-scope compliant coaches (1st May 2026): {in_scope_compliant}
- Total coaches (1st May 2026): {all_coaches}
- Actual proportion: {actual_proportion}%
- MTE minimum proportion: {mte_minimum}%
- MTE compliant on 1st May 2026: {was_compliant}

**GENERATE A CERTIFICATE WITH THESE SECTIONS:**

1. **HEADER SECTION** (use === dividers):
   - Title: "EQUALITY ACT 2010 - ORDER OF THE SECRETARY OF STATE UNDER SECTION 178"
   - Operator details in table format
   - Full authorization statement from Secretary of State
   - Signature block: "Liz Wilson, Deputy Director, Accessibility, Coaches, Taxis and Community Transport Division"
   - Issue Date: {issue_date}
   - Expiry Date: {expiry_date}

2. **TERMS AND CONDITIONS SECTION**:
   - Title: "PUBLIC SERVICE VEHICLES ACCESSIBILITY REGULATIONS 2000 - SPECIAL AUTHORISATION TERMS AND CONDITIONS OF USE"
   - All 11 numbered validity conditions
   - In condition 8a, specify: "The applicable minimum proportion is {minimum_fleet_proportion}% and will be fixed for this operator"
   - Include definitions of "relevant vehicle" and "relevant service"
   - Include all sub-conditions (a, b, c, etc.)

3. **SCHEDULE A: MINIMUM FLEET PROPORTION**:
   - State the minimum fleet proportion: {minimum_fleet_proportion}%
   - Explain it's calculated as the higher of:
     a) Actual in-scope compliant proportion
     b) MTE minimum requirement proportion
   - Show calculation breakdown:
     * In-scope compliant coaches: {in_scope_compliant}
     * Total coaches: {all_coaches}
     * Actual proportion: {actual_proportion}%
     * MTE minimum proportion: {mte_minimum}%
     * Selected: {minimum_fleet_proportion}% (the higher value)
   - State whether operator met/exceeded MTE requirements
   - If was_compliant is false, add: "⚠️ IMPORTANT VALIDITY CONDITION: This certificate is GRANTED but NOT VALID for use until the operator achieves the minimum fleet proportion of {minimum_fleet_proportion}%. This certificate CANNOT be used to provide home-to-school services using non-compliant vehicles until this threshold is met."

4. **SCHEDULE B: LIST OF RELEVANT VEHICLES**:
   - Create a table with columns: Operator Name | Operator Licence Number | Vehicle Registration | Vehicle Chassis Number
   - One row per vehicle from the vehicles list
   - Format: {operator_name} | {operator_licence_number} | {registration} | {vin}

5. **IMPORTANT NOTES SECTION**:
   - Certificate must be carried onboard vehicles
   - Operator must maintain {minimum_fleet_proportion}% compliant coaches
   - Alternative accessible transport requirements
   - Valid until {expiry_date} unless withdrawn
   - Partial compliance requirements for non-compliant vehicles

**FORMATTING:**
- Use "================" as section dividers (80 characters wide)
- Use proper indentation for sub-sections
- Number all conditions clearly
- Use formal legal language throughout
- Include all statutory references
- Make it look like an official UK government legal document

Generate the complete certificate now."""],
        output_schema=None  # Free-form text output
    )
    
    # Map inputs to prompt variables
    generate_cert.map_input(
        input_variable="operator_name",
        expression="flow.input.operator_name"
    )
    generate_cert.map_input(
        input_variable="operator_licence_number",
        expression="flow.input.operator_licence_number"
    )
    generate_cert.map_input(
        input_variable="service_reference",
        expression="flow.input.service_reference"
    )
    generate_cert.map_input(
        input_variable="band",
        expression="flow.input.band"
    )
    generate_cert.map_input(
        input_variable="minimum_fleet_proportion",
        expression="flow.input.minimum_fleet_proportion"
    )
    generate_cert.map_input(
        input_variable="issue_date",
        expression="flow.input.issue_date"
    )
    generate_cert.map_input(
        input_variable="expiry_date",
        expression="flow.input.expiry_date"
    )
    
    # Format vehicles list for prompt
    generate_cert.map_input(
        input_variable="vehicles_list",
        expression="'\\n'.join([f'{i+1}. Registration: {v[\"registration\"]}, VIN: {v[\"vin\"]}' for i, v in enumerate(flow.input.vehicles)])"
    )
    
    # Map calculation details
    generate_cert.map_input(
        input_variable="in_scope_compliant",
        expression="flow.input.calculation_details['in_scope_compliant_coaches_may_2026']"
    )
    generate_cert.map_input(
        input_variable="all_coaches",
        expression="flow.input.calculation_details['all_coaches_may_2026']"
    )
    generate_cert.map_input(
        input_variable="actual_proportion",
        expression="flow.input.calculation_details['actual_proportion']"
    )
    generate_cert.map_input(
        input_variable="mte_minimum",
        expression="flow.input.calculation_details['mte_minimum_proportion']"
    )
    generate_cert.map_input(
        input_variable="was_compliant",
        expression="'Yes' if flow.input.calculation_details['was_mte_compliant'] else 'No'"
    )
    
    # Create summary node
    create_summary = aflow.prompt(
        name="create_summary",
        system_prompt="You are a document summarizer. Create brief, clear summaries of certificates.",
        user_prompt=["Create a 2-3 sentence summary of this PSVAR exemption certificate for {operator_name}. Include the service reference, validity dates, number of vehicles, and minimum fleet proportion requirement."],
        output_schema=None
    )
    
    create_summary.map_input(
        input_variable="operator_name",
        expression="flow.input.operator_name"
    )
    
    # Sequence the flow
    aflow.sequence(START, generate_cert, create_summary, END)
    
    # Map outputs
    aflow.map_output(
        output_variable="success",
        expression="True"
    )
    aflow.map_output(
        output_variable="certificate_text",
        expression="flow['generate_certificate'].output"
    )
    aflow.map_output(
        output_variable="certificate_summary",
        expression="flow['create_summary'].output"
    )
    aflow.map_output(
        output_variable="operator_name",
        expression="flow.input.operator_name"
    )
    aflow.map_output(
        output_variable="service_reference",
        expression="flow.input.service_reference"
    )
    aflow.map_output(
        output_variable="minimum_fleet_proportion",
        expression="flow.input.minimum_fleet_proportion"
    )
    aflow.map_output(
        output_variable="is_valid_immediately",
        expression="flow.input.calculation_details['was_mte_compliant']"
    )
    aflow.map_output(
        output_variable="validity_status",
        expression="'Certificate is VALID immediately' if flow.input.calculation_details['was_mte_compliant'] else 'Certificate GRANTED but NOT VALID until minimum fleet proportion is achieved'"
    )
    aflow.map_output(
        output_variable="issue_date",
        expression="flow.input.issue_date"
    )
    aflow.map_output(
        output_variable="expiry_date",
        expression="flow.input.expiry_date"
    )
    aflow.map_output(
        output_variable="vehicle_count",
        expression="len(flow.input.vehicles)"
    )
    aflow.map_output(
        output_variable="band",
        expression="flow.input.band"
    )
    
    return aflow

# Made with Bob
