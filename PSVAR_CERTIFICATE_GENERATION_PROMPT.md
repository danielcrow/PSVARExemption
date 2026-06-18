# PSVAR Exemption Certificate Generation Prompt

## Purpose
This document provides a comprehensive prompt template for generating official PSVAR (Public Service Vehicles Accessibility Regulations) exemption certificates under Section 178 of the Equality Act 2010.

---

## Certificate Structure

The certificate consists of:
1. **Front Page** - Operator details, authorization statement, and signatures
2. **Terms and Conditions** - 11 validity conditions
3. **Schedule A** - Minimum fleet proportion calculation
4. **Schedule B** - List of relevant vehicles

---

## Input Data Required

```json
{
  "operator_name": "string",
  "operator_licence_number": "string",
  "service_reference": "string",
  "band": "A|B|C|D",
  "minimum_fleet_proportion": "float (percentage)",
  "issue_date": "DD/MM/YYYY",
  "expiry_date": "DD/MM/YYYY",
  "vehicles": [
    {
      "registration": "string (e.g., AB12 CDE)",
      "vin": "string (17-character VIN/Chassis Number)"
    }
  ],
  "calculation_details": {
    "in_scope_compliant_coaches_may_2026": "integer",
    "all_coaches_may_2026": "integer",
    "actual_proportion": "float",
    "mte_minimum_proportion": "float",
    "was_mte_compliant": "boolean"
  }
}
```

---

## Generative Prompt Template

```
You are an official document generator for the UK Department for Transport. Generate a formal PSVAR exemption certificate under Section 178 of the Equality Act 2010.

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

**CALCULATION CONTEXT:**
- In-scope compliant coaches (1st May 2026): {in_scope_compliant_coaches_may_2026}
- Total coaches (1st May 2026): {all_coaches_may_2026}
- Actual proportion: {actual_proportion}%
- MTE minimum proportion: {mte_minimum_proportion}%
- MTE compliant on 1st May 2026: {was_mte_compliant}

**GENERATE:**
A complete, formal exemption certificate following the official UK government format with:

1. **HEADER SECTION**
   - Title: "EQUALITY ACT 2010 - ORDER OF THE SECRETARY OF STATE UNDER SECTION 178"
   - Operator details table
   - Authorization statement
   - Signature block (Liz Wilson, Deputy Director)
   - Issue and expiry dates

2. **TERMS AND CONDITIONS SECTION**
   - All 11 validity conditions
   - Specific minimum fleet proportion: {minimum_fleet_proportion}%
   - Definition of "relevant vehicle" and "relevant service"
   - Compliance requirements

3. **SCHEDULE A: MINIMUM FLEET PROPORTION**
   - Explanation of calculation method
   - Statement that proportion is fixed for certificate validity
   - Reference to MTE scheme

4. **SCHEDULE B: LIST OF RELEVANT VEHICLES**
   - Table format with columns:
     * Operator Name
     * Operator Licence Number
     * Vehicle Registration
     * Vehicle Chassis Number
   - One row per vehicle

5. **IMPORTANT NOTES SECTION**
   - Certificate carrying requirements
   - Fleet proportion maintenance requirement
   - Alternative transport requirements
   - Validity conditions

**FORMATTING REQUIREMENTS:**
- Use formal, legal language
- Include section dividers (================)
- Use proper indentation and numbering
- Include all statutory references
- Maintain professional government document style
- Use clear paragraph breaks
- Include all required legal disclaimers

**TONE:**
- Authoritative and official
- Legally precise
- Clear and unambiguous
- Formal UK government style
```

---

## Complete Example Certificate

### Input Data:
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

### Generated Certificate:

```
================================================================================
                    EQUALITY ACT 2010
         ORDER OF THE SECRETARY OF STATE UNDER SECTION 178
================================================================================

Operator:           ABC Coaches Limited
O Licence:          OD1234567
Band:               C
Service Reference:  PSVAR-2026-001

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

30/07/2025

Liz Wilson
Deputy Director
Accessibility, Coaches, Taxis and Community Transport Division

Issue Date: 30/07/2025
Expiry Date: 30/07/2027

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
      proportion is 20.0% and will be fixed for this operator for the 
      validity of Special Authorisations applied to their coaches.

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
      on or after 1st February 2027, or pre registered on or after 1st August 
      2026 but not delivered to its first owner until or after 1st February 
      2027.

   e. Fulfilment of requests for PSVAR compliant vehicles:
      Upon receipt of a valid request the Operator will arrange for an 
      available coach compliant with PSVAR to be provided. A valid request is:
      i.   A request made by a commissioner of home to school services, such 
           as a local authority, school or group of parents;
      ii.  A request for a coach, designed to carry over twenty two 
           passengers, which complies with the Public Service Vehicles 
           Accessibility Regulations 2000;
      iii. A request made in order to transport a specific person who could 
           not use that vehicle if it did not comply with PSVAR, or who could 
           not do so safely or in reasonable comfort.

   f. A coach is considered to be available if it is owned or leased by the 
      operator and it has not already been procured to provide a Relevant 
      Service.

   g. Operators must not charge or propose to charge more to provide a PSVAR
      compliant vehicle than they would to provide a non-compliant vehicle.

   h. A valid request for a PSVAR compliant vehicle is fulfilled by a date 
      two calendar months or more following the request being made.

9. The operator obtains from the commissioner of Relevant Services confirmation
   that alternative accessible services will be provided for passengers who 
   cannot use a Relevant Service because it is provided using a Relevant 
   Vehicle, and where they operate a Relevant Service of their own volition, 
   they make arrangements for the provision of such alternative accessible 
   services themselves.

10. This Order supersedes any Orders previously issued in relation to Relevant
    Vehicles.

11. The failure by the operator of a Relevant Vehicle to comply with these 
    terms will render any Special Authorisation applicable to the vehicles 
    they operate invalid, and leave the operator subject to enforcement action.

================================================================================
                    SCHEDULE A: MINIMUM FLEET PROPORTION
================================================================================

The Minimum fleet proportion of 20.0% has been calculated as the higher of:

1. The combined total of PSVAR compliant coaches operated on home to school
   and rail replacement services, as a proportion of the total coach fleet; or

2. The combined total of PSVAR compliant coaches which the operator was, or
   would have been, required to operate on home to school and rail replacement
   services by the terms of the original Medium Term Exemption scheme, as a
   proportion of the total coach fleet.

CALCULATION DETAILS:
- In-scope compliant coaches on 1st May 2026: 2
- Total coaches on 1st May 2026: 10
- Actual proportion: 20.0%
- MTE minimum proportion: 10.0%
- Selected proportion: 20.0% (actual proportion is higher)

The operator exceeded the Medium Term Exemption requirements on 1st May 2026.

This proportion is fixed for the validity of this Special Authorisation.

================================================================================
                    SCHEDULE B: LIST OF RELEVANT VEHICLES
================================================================================

This Order grants Special Authorisations for the following vehicles:

Operator Name         | Operator Licence | Vehicle Registration | Vehicle Chassis Number
ABC Coaches Limited   | OD1234567        | AB12 CDE            | 1HGBH41JXMN109186
ABC Coaches Limited   | OD1234567        | FG34 HIJ            | 2HGBH41JXMN109187

================================================================================
                              END OF CERTIFICATE
================================================================================

IMPORTANT NOTES:

1. This certificate must be carried onboard each relevant vehicle when 
   providing relevant services.

2. The operator must maintain the minimum fleet proportion of 20.0% 
   PSVAR compliant coaches across their entire coach fleet.

3. Alternative accessible transport must be available for passengers who 
   cannot use non-compliant vehicles.

4. This certificate is valid until 30/07/2027 unless withdrawn by the 
   Secretary of State or the operator fails to comply with the validity 
   conditions.

5. Any relevant vehicles used on relevant services must be at least 
   "Partially Compliant" with PSVAR Schedule 3 (2)-(5).

6. New vehicles registered on or after 1st February 2027 must be "PSVAR 
   enabled" as defined in the validity conditions.

================================================================================
```

---

## Conditional Certificate Text

### If Operator Was NOT MTE Compliant on 1st May 2026

Add this warning section after Schedule A:

```
⚠️ IMPORTANT VALIDITY CONDITION:

This certificate is GRANTED but NOT VALID for use until the operator achieves 
the minimum fleet proportion of {minimum_fleet_proportion}%.

On 1st May 2026, the operator had {in_scope_compliant_coaches_may_2026} 
compliant coaches but was required to have {mte_minimum_coaches} compliant 
coaches under the Medium Term Exemption scheme.

This certificate CANNOT be used to provide home-to-school services using 
non-compliant vehicles until the operator achieves and maintains the minimum 
fleet proportion of {minimum_fleet_proportion}%.

The operator must notify the Department for Transport when they achieve this 
threshold to activate the certificate.
```

---

## Validation Checklist

Before generating certificate, verify:

- ✅ Operator name and licence number are valid
- ✅ All vehicle VINs are 17 characters
- ✅ All vehicle registrations follow UK format
- ✅ Minimum fleet proportion is calculated correctly
- ✅ Issue date is not in the future
- ✅ Expiry date is after issue date
- ✅ Band (A/B/C/D) matches fleet size
- ✅ Service reference is unique
- ✅ At least one vehicle is listed in Schedule B

---

## API Integration Format

For programmatic generation:

```python
from tools.generate_exemption_certificate import generate_exemption_certificate, CertificateData, VehicleEntry

certificate_data = CertificateData(
    operator_name="ABC Coaches Limited",
    operator_licence_number="OD1234567",
    service_reference="PSVAR-2026-001",
    vehicles=[
        VehicleEntry(registration="AB12 CDE", vin="1HGBH41JXMN109186"),
        VehicleEntry(registration="FG34 HIJ", vin="2HGBH41JXMN109187")
    ],
    minimum_fleet_proportion=20.0,
    band="C",
    issue_date="30/07/2025",
    expiry_date="30/07/2027"
)

result = generate_exemption_certificate(certificate_data)
print(result.certificate_text)
```

---

## Output Formats

### 1. Plain Text (Default)
- ASCII text with line breaks
- Suitable for printing
- Can be saved as .txt file

### 2. PDF (Recommended for Official Use)
- Professional formatting
- Official letterhead
- Digital signatures
- Watermarks

### 3. HTML (Web Display)
- Styled with CSS
- Responsive design
- Printable version

### 4. JSON (Data Exchange)
- Structured data
- API responses
- Database storage

---

## Legal Requirements

The certificate MUST include:

1. ✅ Section 178 reference (Equality Act 2010)
2. ✅ Secretary of State authorization
3. ✅ Signature block (Liz Wilson, Deputy Director)
4. ✅ Issue and expiry dates
5. ✅ All 11 validity conditions
6. ✅ Minimum fleet proportion (specific percentage)
7. ✅ Schedule A calculation explanation
8. ✅ Schedule B complete vehicle list
9. ✅ Definition of "relevant vehicle"
10. ✅ Definition of "relevant service"
11. ✅ Withdrawal clause
12. ✅ Enforcement warning

---

## Usage Examples

### Example 1: Small Operator (Band A)
```
Operator: Village Coaches
Vehicles: 3
In-scope coaches: 5
Minimum proportion: 20%
Certificate valid immediately
```

### Example 2: Medium Operator (Band C)
```
Operator: County Transport
Vehicles: 15
In-scope coaches: 20
Minimum proportion: 12.5%
Certificate valid immediately
```

### Example 3: Large Operator (Band D) - Non-compliant
```
Operator: National Coaches Ltd
Vehicles: 50
In-scope coaches: 35
Minimum proportion: 15%
Certificate GRANTED BUT NOT VALID until threshold met
```

---

## Document Metadata

- **Authority**: Secretary of State for Transport
- **Legislation**: Equality Act 2010, Section 178
- **Regulations**: Public Service Vehicles Accessibility Regulations 2000
- **Issuing Office**: Accessibility, Coaches, Taxis and Community Transport Division
- **Signatory**: Liz Wilson, Deputy Director
- **Standard Validity**: 2 years from issue date
- **Reference Date**: 1st May 2026 (for fleet calculations)

---

*Document Version: 1.0*  
*Based on: Draft exemption terms including minimum fleet calculation*  
*Template Date: June 2026*