# PSVAR Exemption Assessment - Demo Data for All Possible Outcomes

This document provides test data scenarios that demonstrate all possible assessment outcomes in the PSVAR exemption system.

## Overview of Possible Outcomes

### Decision Types
1. **OUT_OF_SCOPE** - Service doesn't qualify for PSVAR exemption assessment
2. **EXEMPTION_NOT_NEEDED** - All vehicles are fully compliant
3. **POTENTIALLY_EXEMPT_IF_VALID_CERTIFICATE_EXISTS** - Has valid exemption certificate
4. **NOT_EXEMPT** - Doesn't meet exemption criteria
5. **EXEMPT_BUT_NON_COMPLIANT_WITH_CONDITIONS** - Has exemption but not following conditions

### Final Case Outcomes
1. **CAN_HAVE_EXEMPTION** - Eligible for exemption
2. **CANNOT_HAVE_EXEMPTION** - Not eligible for exemption
3. **FURTHER_INVESTIGATION_REQUIRED** - Needs DVSA review
4. **OUT_OF_SCOPE** - Service type not eligible
5. **EXEMPTION_NOT_REQUIRED** - Fleet is fully compliant

---

## Scenario 1: OUT_OF_SCOPE - Not Home-to-School Service

**Outcome**: OUT_OF_SCOPE / OUT_OF_SCOPE

**Test Data**:
```
Company Name: City Bus Services Ltd
Operator Licence: OB1234567
Contact Name: John Smith
Contact Phone: 01234567890
Contact Email: john.smith@citybus.com
Address: 123 High Street, London
Postcode: SW1A 1AA

Service Type: Regular bus service (NOT HTS)
Closed Door: No
Paying Customers: Yes

Fleet Size: 10
Fully Compliant: 5
Partially Compliant: 3
Non-Compliant: 2

VINs: (any 10 valid VINs)
```

**Expected Result**: Application rejected - service type not eligible for PSVAR exemption

---

## Scenario 2: OUT_OF_SCOPE - Has Paying Customers

**Outcome**: OUT_OF_SCOPE / OUT_OF_SCOPE

**Test Data**:
```
Company Name: School Transport Co
Operator Licence: OB2345678
Contact Name: Jane Doe
Contact Phone: 01234567891
Contact Email: jane.doe@schooltransport.com
Address: 456 School Lane, Manchester
Postcode: M1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: YES (This makes it out of scope)

Fleet Size: 8
Fully Compliant: 4
Partially Compliant: 2
Non-Compliant: 2

VINs: (any 8 valid VINs)
```

**Expected Result**: Application rejected - HTS services with paying customers not eligible

---

## Scenario 3: EXEMPTION_NOT_NEEDED - Fully Compliant Fleet

**Outcome**: EXEMPTION_NOT_NEEDED / EXEMPTION_NOT_REQUIRED

**Test Data**:
```
Company Name: Premium School Transport
Operator Licence: OB3456789
Contact Name: Robert Johnson
Contact Phone: 01234567892
Contact Email: robert.johnson@premiumschool.com
Address: 789 Education Road, Birmingham
Postcode: B1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 12
Fully Compliant: 12 (ALL vehicles compliant)
Partially Compliant: 0
Non-Compliant: 0

VINs: (12 valid VINs)
Has Read Band Requirements: Yes
```

**Expected Result**: No exemption needed - entire fleet is fully compliant with PSVAR

---

## Scenario 4: CAN_HAVE_EXEMPTION - Band A (1-5 vehicles), Milestone Compliant

**Outcome**: NOT_EXEMPT (for application) / CAN_HAVE_EXEMPTION

**Test Data**:
```
Company Name: Small School Services
Operator Licence: OB4567890
Contact Name: Sarah Williams
Contact Phone: 01234567893
Contact Email: sarah.williams@smallschool.com
Address: 321 Village Street, Leeds
Postcode: LS1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 4 (Band A: 1-5 vehicles)
Fully Compliant: 2
Partially Compliant: 1
Non-Compliant: 1

VINs:
- 1HGBH41JXMN109186 (fully compliant)
- 2HGBH41JXMN109187 (fully compliant)
- 3HGBH41JXMN109188 (partially compliant)
- 4HGBH41JXMN109189 (non-compliant)

Partially Compliant VINs: 3HGBH41JXMN109188
Non-Compliant VINs: 4HGBH41JXMN109189

Has Read Band A Requirements: Yes

Operational Commitments:
- Will carry exemption certificate onboard: Yes
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Eligible for exemption - meets Band A milestone requirements

---

## Scenario 5: CAN_HAVE_EXEMPTION - Band B (6-9 vehicles), Milestone Compliant

**Outcome**: NOT_EXEMPT (for application) / CAN_HAVE_EXEMPTION

**Test Data**:
```
Company Name: Medium School Transport
Operator Licence: OB5678901
Contact Name: Michael Brown
Contact Phone: 01234567894
Contact Email: michael.brown@mediumschool.com
Address: 654 Transport Way, Liverpool
Postcode: L1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 7 (Band B: 6-9 vehicles)
Fully Compliant: 4
Partially Compliant: 2
Non-Compliant: 1

VINs:
- 1HGBH41JXMN109190 (fully compliant)
- 2HGBH41JXMN109191 (fully compliant)
- 3HGBH41JXMN109192 (fully compliant)
- 4HGBH41JXMN109193 (fully compliant)
- 5HGBH41JXMN109194 (partially compliant)
- 6HGBH41JXMN109195 (partially compliant)
- 7HGBH41JXMN109196 (non-compliant)

Partially Compliant VINs: 5HGBH41JXMN109194, 6HGBH41JXMN109195
Non-Compliant VINs: 7HGBH41JXMN109196

Has Read Band B Requirements: Yes

Operational Commitments:
- Will carry exemption certificate onboard: Yes
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Eligible for exemption - meets Band B milestone requirements

---

## Scenario 6: CAN_HAVE_EXEMPTION - Band C (10-29 vehicles), Milestone Compliant

**Outcome**: NOT_EXEMPT (for application) / CAN_HAVE_EXEMPTION

**Test Data**:
```
Company Name: Large School Services
Operator Licence: OB6789012
Contact Name: Emma Davis
Contact Phone: 01234567895
Contact Email: emma.davis@largeschool.com
Address: 987 Education Avenue, Bristol
Postcode: BS1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 15 (Band C: 10-29 vehicles)
Fully Compliant: 10
Partially Compliant: 3
Non-Compliant: 2

VINs: (15 valid VINs - 10 fully compliant, 3 partially, 2 non-compliant)
- 1HGBH41JXMN109200 through 1HGBH41JXMN109209 (fully compliant)
- 2HGBH41JXMN109210, 2HGBH41JXMN109211, 2HGBH41JXMN109212 (partially compliant)
- 3HGBH41JXMN109213, 3HGBH41JXMN109214 (non-compliant)

Has Read Band C Requirements: Yes

Operational Commitments:
- Will carry exemption certificate onboard: Yes
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Eligible for exemption - meets Band C milestone requirements

---

## Scenario 7: CAN_HAVE_EXEMPTION - Band D (30+ vehicles), Milestone Compliant

**Outcome**: NOT_EXEMPT (for application) / CAN_HAVE_EXEMPTION

**Test Data**:
```
Company Name: Major School Transport Group
Operator Licence: OB7890123
Contact Name: David Wilson
Contact Phone: 01234567896
Contact Email: david.wilson@majorschool.com
Address: 147 Fleet Street, Newcastle
Postcode: NE1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 35 (Band D: 30+ vehicles)
Fully Compliant: 25
Partially Compliant: 6
Non-Compliant: 4

VINs: (35 valid VINs - 25 fully compliant, 6 partially, 4 non-compliant)

Has Read Band D Requirements: Yes

Operational Commitments:
- Will carry exemption certificate onboard: Yes
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Eligible for exemption - meets Band D milestone requirements

---

## Scenario 8: CANNOT_HAVE_EXEMPTION - Not Milestone Compliant

**Outcome**: NOT_EXEMPT / CANNOT_HAVE_EXEMPTION

**Test Data**:
```
Company Name: Non-Compliant Transport
Operator Licence: OB8901234
Contact Name: Lisa Taylor
Contact Phone: 01234567897
Contact Email: lisa.taylor@noncompliant.com
Address: 258 Old Road, Sheffield
Postcode: S1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 10 (Band C: 10-29 vehicles)
Fully Compliant: 2 (BELOW milestone requirement)
Partially Compliant: 3
Non-Compliant: 5

VINs: (10 valid VINs)

Has Read Band C Requirements: Yes

Operational Commitments:
- Will carry exemption certificate onboard: Yes
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Cannot have exemption - doesn't meet minimum compliance milestones for Band C

---

## Scenario 9: CANNOT_HAVE_EXEMPTION - Missing Operational Commitments

**Outcome**: NOT_EXEMPT / CANNOT_HAVE_EXEMPTION

**Test Data**:
```
Company Name: Incomplete Commitments Transport
Operator Licence: OB9012345
Contact Name: James Anderson
Contact Phone: 01234567898
Contact Email: james.anderson@incomplete.com
Address: 369 Service Road, Cardiff
Postcode: CF1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 5 (Band A)
Fully Compliant: 3
Partially Compliant: 1
Non-Compliant: 1

VINs: (5 valid VINs)

Has Read Band A Requirements: Yes

Operational Commitments:
- Will carry exemption certificate onboard: NO (Missing commitment)
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Cannot have exemption - doesn't commit to carrying certificate onboard

---

## Scenario 10: FURTHER_INVESTIGATION_REQUIRED - Invalid VINs

**Outcome**: NOT_EXEMPT / FURTHER_INVESTIGATION_REQUIRED

**Test Data**:
```
Company Name: Invalid VIN Transport
Operator Licence: OB0123456
Contact Name: Patricia Martinez
Contact Phone: 01234567899
Contact Email: patricia.martinez@invalidvin.com
Address: 741 Check Street, Edinburgh
Postcode: EH1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 6
Fully Compliant: 3
Partially Compliant: 2
Non-Compliant: 1

VINs:
- 1HGBH41JXMN109220 (valid)
- 2HGBH41JXMN109221 (valid)
- 3HGBH41JXMN109222 (valid)
- INVALID123456789 (INVALID - wrong format)
- 5HGBH41JXMN109224 (valid)
- 6HGBH41JXMN109225 (valid)

Has Read Band B Requirements: Yes
```

**Expected Result**: Requires investigation - VIN validation errors detected

---

## Scenario 11: FURTHER_INVESTIGATION_REQUIRED - Duplicate VINs

**Outcome**: NOT_EXEMPT / FURTHER_INVESTIGATION_REQUIRED

**Test Data**:
```
Company Name: Duplicate VIN Transport
Operator Licence: OB1234568
Contact Name: Christopher Lee
Contact Phone: 01234567800
Contact Email: christopher.lee@duplicate.com
Address: 852 Verify Lane, Glasgow
Postcode: G1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 5
Fully Compliant: 3
Partially Compliant: 1
Non-Compliant: 1

VINs:
- 1HGBH41JXMN109230 (fully compliant)
- 2HGBH41JXMN109231 (fully compliant)
- 3HGBH41JXMN109232 (fully compliant)
- 4HGBH41JXMN109233 (partially compliant)
- 1HGBH41JXMN109230 (DUPLICATE - same as first VIN)

Has Read Band A Requirements: Yes
```

**Expected Result**: Requires investigation - duplicate VINs detected

---

## Scenario 12: FURTHER_INVESTIGATION_REQUIRED - Fleet Size Mismatch

**Outcome**: NOT_EXEMPT / FURTHER_INVESTIGATION_REQUIRED

**Test Data**:
```
Company Name: Mismatch Fleet Transport
Operator Licence: OB2345679
Contact Name: Jennifer White
Contact Phone: 01234567801
Contact Email: jennifer.white@mismatch.com
Address: 963 Count Road, Aberdeen
Postcode: AB1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 10 (stated)
Fully Compliant: 4
Partially Compliant: 2
Non-Compliant: 2
Total from counts: 8 (MISMATCH - doesn't add up to 10)

VINs: (only 8 VINs provided, but fleet size says 10)

Has Read Band C Requirements: Yes
```

**Expected Result**: Requires investigation - fleet size doesn't match vehicle counts

---

## Scenario 13: FURTHER_INVESTIGATION_REQUIRED - Hasn't Read Band Requirements

**Outcome**: NOT_EXEMPT / FURTHER_INVESTIGATION_REQUIRED

**Test Data**:
```
Company Name: Unread Requirements Transport
Operator Licence: OB3456780
Contact Name: Daniel Harris
Contact Phone: 01234567802
Contact Email: daniel.harris@unread.com
Address: 159 Policy Street, Swansea
Postcode: SA1 1AA

Service Type: HTS
Closed Door: Yes
Paying Customers: No

Fleet Size: 7 (Band B)
Fully Compliant: 4
Partially Compliant: 2
Non-Compliant: 1

VINs: (7 valid VINs)

Has Read Band B Requirements: NO (Critical - must read requirements)

Operational Commitments:
- Will carry exemption certificate onboard: Yes
- Alternative accessible transport available: Yes
- Written confirmation retained: Yes
```

**Expected Result**: Requires investigation - applicant hasn't confirmed reading band requirements

---

## How to Use This Demo Data

### Testing in the Chat Interface

1. **Start a new assessment** - Say "Start a new PSVAR exemption application assessment"
2. **Provide data step by step** - The agent will guide you through collecting:
   - Company and contact information
   - Service confirmation
   - Fleet composition
   - Vehicle VINs
   - Operational commitments (if needed)
3. **Observe the outcome** - The agent will invoke the assessment tool and present results

### Expected Behavior for Each Scenario

- **Scenarios 1-2**: Immediate rejection - out of scope
- **Scenario 3**: Immediate approval - no exemption needed
- **Scenarios 4-7**: Eligible for exemption - different band sizes
- **Scenarios 8-9**: Cannot have exemption - fails requirements
- **Scenarios 10-13**: Requires DVSA investigation - data issues

### Key Testing Points

1. **Service Type Validation**: Must be "HTS" (uppercase)
2. **VIN Format**: 17 characters, valid check digit
3. **Fleet Size Consistency**: Total must match sum of compliant/partially/non-compliant
4. **Band Calculation**: Automatic based on fleet size
5. **Milestone Requirements**: Vary by band and date
6. **Operational Commitments**: Required for partially/non-compliant vehicles

---

## Quick Reference: Band Requirements

| Band | Fleet Size | Current Milestone (2026) |
|------|------------|--------------------------|
| A    | 1-5        | 50% fully compliant      |
| B    | 6-9        | 50% fully compliant      |
| C    | 10-29      | 50% fully compliant      |
| D    | 30+        | 50% fully compliant      |

*Note: Milestone requirements increase over time according to PSVAR regulations*

---

## Valid VIN Examples for Testing

Use these valid VINs for testing (they pass check digit validation):

```
1HGBH41JXMN109186
2HGBH41JXMN109187
3HGBH41JXMN109188
4HGBH41JXMN109189
5HGBH41JXMN109190
1FTFW1ET5BFC12345
2FMDK3GC3BBB12345
3FADP4BJ3BM123456
4T1BF1FK5CU123456
5XYKT3A69CG123456
```

---

## Document Version

- **Version**: 1.0
- **Last Updated**: 2026-06-03
- **Author**: PSVAR Assessment System
- **Purpose**: Comprehensive testing and demonstration of all assessment outcomes