# PSVAR Certificate Generation - Simple Prompt

## Quick Start Prompt

```
You are an official UK government document generator. Generate a formal PSVAR exemption certificate using the following data:

{paste_json_data_here}

Generate a complete, formal exemption certificate following the official UK Department for Transport format with these sections:

1. HEADER: Title, operator details, authorization statement, signature (Liz Wilson, Deputy Director), dates
2. TERMS AND CONDITIONS: All 11 validity conditions with the specific minimum fleet proportion
3. SCHEDULE A: Calculation explanation showing how the minimum fleet proportion was determined
4. SCHEDULE B: Table of all vehicles with operator name, licence number, registration, and VIN
5. IMPORTANT NOTES: Certificate requirements and validity conditions

Use formal legal language, proper formatting with section dividers (====), and include all statutory references.
```

---

## Example Usage

### Input JSON:
```json
{
  "operator_name": "ABC Coaches Limited",
  "operator_licence_number": "OD1234567",
  "service_reference": "PSVAR-2026-001",
  "band": "C",
  "minimum_fleet_proportion": 20.0,
  "issue_date": "30/07/2025",
  "expiry_date": "30/07/2027",
  "vehicles": [
    {
      "registration": "AB12 CDE",
      "vin": "1HGBH41JXMN109186"
    },
    {
      "registration": "FG34 HIJ",
      "vin": "2HGBH41JXMN109187"
    }
  ],
  "calculation_details": {
    "in_scope_compliant_coaches_may_2026": 2,
    "all_coaches_may_2026": 10,
    "actual_proportion": 20.0,
    "mte_minimum_proportion": 10.0,
    "was_mte_compliant": true
  }
}
```

### Prompt to AI:
```
Generate a PSVAR exemption certificate for this application:

{paste the JSON above}

Include:
- Full legal authorization under Section 178, Equality Act 2010
- All 11 validity conditions with 20.0% minimum fleet proportion
- Schedule A showing calculation: actual 20.0% vs MTE minimum 10.0%, selected 20.0%
- Schedule B table with 2 vehicles
- Signature: Liz Wilson, Deputy Director, Accessibility Division
- Valid from 30/07/2025 to 30/07/2027
- Note that operator exceeded MTE requirements on 1st May 2026

Format as official UK government document with proper section dividers.
```

---

## Enhanced Prompt with Conditional Logic

```
Generate a PSVAR exemption certificate using this data:

{paste_json_data_here}

**IMPORTANT CONDITIONAL LOGIC:**

IF calculation_details.was_mte_compliant == true:
  - Certificate is VALID immediately
  - State: "The operator exceeded/met the Medium Term Exemption requirements on 1st May 2026"
  
IF calculation_details.was_mte_compliant == false:
  - Certificate is GRANTED BUT NOT VALID
  - Add warning section after Schedule A:
    "⚠️ IMPORTANT VALIDITY CONDITION: This certificate is GRANTED but NOT VALID 
    for use until the operator achieves the minimum fleet proportion of {minimum_fleet_proportion}%. 
    This certificate CANNOT be used to provide home-to-school services using non-compliant 
    vehicles until this threshold is met."

**SCHEDULE A DETAILS:**
Show calculation breakdown:
- In-scope compliant coaches on 1st May 2026: {in_scope_compliant_coaches_may_2026}
- Total coaches on 1st May 2026: {all_coaches_may_2026}
- Actual proportion: {actual_proportion}%
- MTE minimum proportion: {mte_minimum_proportion}%
- Selected: {minimum_fleet_proportion}% (the higher value)

**SCHEDULE B FORMAT:**
Create table with these exact columns:
| Operator Name | Operator Licence | Vehicle Registration | Vehicle Chassis Number |

One row per vehicle from the vehicles array.

Use formal UK government legal document style throughout.
```

---

## One-Line Prompt (Minimal)

```
Generate a formal PSVAR exemption certificate under Section 178 of the Equality Act 2010 using this data: {json_data}. Include header with operator details and authorization, all 11 validity conditions with the minimum fleet proportion, Schedule A calculation explanation, Schedule B vehicle table, and important notes. Use official UK government document format.
```

---

## Prompt for Non-Compliant Operators

When `was_mte_compliant: false`:

```
Generate a PSVAR exemption certificate with CONDITIONAL VALIDITY for this data:

{paste_json_data_here}

**CRITICAL:** This operator was NOT compliant with MTE requirements on 1st May 2026.

The certificate must include:
1. Standard header and authorization
2. All 11 validity conditions
3. Schedule A with calculation showing:
   - Operator had {in_scope_compliant_coaches_may_2026} compliant coaches
   - MTE required {calculate from mte_minimum_proportion}
   - Minimum fleet proportion: {minimum_fleet_proportion}%
4. **VALIDITY WARNING SECTION** (after Schedule A):
   "⚠️ CERTIFICATE GRANTED BUT NOT VALID
   
   This certificate cannot be used until the operator achieves {minimum_fleet_proportion}% 
   compliant coaches across their fleet. The operator must notify the Department for 
   Transport when this threshold is met to activate the certificate."
5. Schedule B vehicle table
6. Important notes emphasizing conditional validity

Mark clearly that certificate is GRANTED but NOT YET VALID FOR USE.
```

---

## Field Mapping Reference

| JSON Field | Certificate Location | Usage |
|------------|---------------------|-------|
| `operator_name` | Header, Schedule B | Operator identification |
| `operator_licence_number` | Header, Schedule B | Licence reference |
| `service_reference` | Header | Unique certificate ID |
| `band` | Header | Compliance band (A/B/C/D) |
| `minimum_fleet_proportion` | Condition 8a, Schedule A, Notes | Required percentage |
| `issue_date` | Header, signature block | Certificate start date |
| `expiry_date` | Header, Notes | Certificate end date |
| `vehicles[].registration` | Schedule B | Vehicle reg numbers |
| `vehicles[].vin` | Schedule B | Vehicle chassis numbers |
| `calculation_details.in_scope_compliant_coaches_may_2026` | Schedule A | Actual compliant count |
| `calculation_details.all_coaches_may_2026` | Schedule A | Total fleet size |
| `calculation_details.actual_proportion` | Schedule A | Calculated actual % |
| `calculation_details.mte_minimum_proportion` | Schedule A | MTE requirement % |
| `calculation_details.was_mte_compliant` | Schedule A, Validity | Compliance status |

---

## Quick Validation Checklist

Before generating, verify JSON has:
- ✅ `operator_name` (not empty)
- ✅ `operator_licence_number` (format: OD followed by digits)
- ✅ `minimum_fleet_proportion` (number > 0)
- ✅ `issue_date` and `expiry_date` (DD/MM/YYYY format)
- ✅ `vehicles` array (at least 1 vehicle)
- ✅ Each vehicle has `registration` and `vin` (VIN = 17 chars)
- ✅ `calculation_details` object with all fields

---

## Sample Output Structure

```
================================================================================
                    EQUALITY ACT 2010
         ORDER OF THE SECRETARY OF STATE UNDER SECTION 178
================================================================================

Operator:           {operator_name}
O Licence:          {operator_licence_number}
Band:               {band}
Service Reference:  {service_reference}

[Authorization text...]

Signed: {issue_date}
Liz Wilson, Deputy Director

Issue Date: {issue_date}
Expiry Date: {expiry_date}

================================================================================
    TERMS AND CONDITIONS
================================================================================

[11 conditions with specific minimum_fleet_proportion in condition 8a]

================================================================================
    SCHEDULE A: MINIMUM FLEET PROPORTION
================================================================================

Minimum fleet proportion: {minimum_fleet_proportion}%

Calculation:
- In-scope compliant: {in_scope_compliant_coaches_may_2026}
- Total coaches: {all_coaches_may_2026}
- Actual proportion: {actual_proportion}%
- MTE minimum: {mte_minimum_proportion}%
- Selected: {minimum_fleet_proportion}% (higher value)

[If was_mte_compliant == false: add validity warning]

================================================================================
    SCHEDULE B: LIST OF RELEVANT VEHICLES
================================================================================

[Table with all vehicles from vehicles array]

================================================================================
    IMPORTANT NOTES
================================================================================

[Standard notes with specific minimum_fleet_proportion and expiry_date]
```

---

## Integration with Existing Tool

To use programmatically with the existing Python tool:

```python
import json
from tools.generate_exemption_certificate import generate_exemption_certificate, CertificateData, VehicleEntry

# Load your JSON data
with open('application_data.json') as f:
    data = json.load(f)

# Convert to CertificateData
certificate_data = CertificateData(
    operator_name=data['operator_name'],
    operator_licence_number=data['operator_licence_number'],
    service_reference=data['service_reference'],
    vehicles=[VehicleEntry(**v) for v in data['vehicles']],
    minimum_fleet_proportion=data['minimum_fleet_proportion'],
    band=data['band'],
    issue_date=data['issue_date'],
    expiry_date=data['expiry_date']
)

# Generate certificate
result = generate_exemption_certificate(certificate_data)

# Output
print(result.certificate_text)
print(f"\n{result.message}")
```

---

## Tips for Best Results

1. **Always include all JSON fields** - missing fields may cause incomplete certificates
2. **Use exact date format** - DD/MM/YYYY (e.g., 30/07/2025)
3. **Verify VINs** - Must be exactly 17 characters
4. **Check band** - Must be A, B, C, or D
5. **Validate percentages** - minimum_fleet_proportion should match calculation
6. **Include calculation_details** - Provides context for Schedule A
7. **Check was_mte_compliant** - Determines certificate validity status

---

*This simplified prompt works directly with your collected JSON data structure to generate official PSVAR exemption certificates.*