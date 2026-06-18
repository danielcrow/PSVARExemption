# PSVAR Schedule A Calculation - Generative Prompt Structure

## Purpose
This document provides a logical calculation structure for determining the minimum fleet proportion that operators must maintain to be eligible for PSVAR exemption certificates. This can be used in generative AI prompts with operator data.

---

## Input Data Required

```json
{
  "operator_name": "string",
  "operator_licence_number": "string",
  "reference_date": "2026-05-01",
  "in_scope_compliant_coaches_may_2026": "integer (≥0)",
  "in_scope_total_coaches_may_2026": "integer (>0)",
  "all_coaches_may_2026": "integer (>0)",
  "current_compliant_coaches": "integer (≥0)",
  "current_total_coaches": "integer (>0)"
}
```

### Field Definitions

1. **in_scope_compliant_coaches_may_2026**: Total number of fully PSVAR compliant coaches used on 1st May 2026 to provide home-to-school (HTS) and rail replacement (RR) services combined

2. **in_scope_total_coaches_may_2026**: Total number of coaches (compliant + non-compliant) used on 1st May 2026 to provide HTS and RR services combined

3. **all_coaches_may_2026**: Total number of coaches used on 1st May 2026 to provide ANY service (including HTS, RR, private hire, touring, etc.)

4. **current_compliant_coaches**: Current number of fully PSVAR compliant coaches in the entire fleet

5. **current_total_coaches**: Current total number of coaches in the entire fleet

---

## Calculation Logic

### Step 1: Calculate Actual In-Scope Compliant Proportion

```
actual_proportion = (in_scope_compliant_coaches_may_2026 / all_coaches_may_2026) × 100
```

**Example:**
- In-scope compliant coaches: 2
- All coaches: 10
- Actual proportion: (2 / 10) × 100 = **20%**

---

### Step 2: Determine MTE Minimum Requirement

Based on the number of in-scope coaches on 1st May 2026, determine the minimum number of compliant coaches required:

```
IF in_scope_total_coaches_may_2026 >= 1 AND <= 5:
    minimum_compliant_coaches = 1

ELSE IF in_scope_total_coaches_may_2026 >= 6 AND <= 9:
    minimum_compliant_coaches = 2

ELSE IF in_scope_total_coaches_may_2026 >= 10 AND <= 29:
    minimum_compliant_coaches = ROUND_UP(in_scope_total_coaches_may_2026 × 0.25)

ELSE IF in_scope_total_coaches_may_2026 >= 30:
    minimum_compliant_coaches = ROUND_UP(in_scope_total_coaches_may_2026 × 0.35)
```

**Rounding Rule**: Always round UP, even for decimals < 0.5
- Example: 1.3 coaches → 2 coaches
- Example: 7.1 coaches → 8 coaches

---

### Step 3: Calculate MTE Minimum Proportion

```
mte_minimum_proportion = (minimum_compliant_coaches / all_coaches_may_2026) × 100
```

**Example:**
- Minimum compliant coaches required: 5
- All coaches: 40
- MTE minimum proportion: (5 / 40) × 100 = **12.5%**

---

### Step 4: Select Higher Proportion

```
minimum_fleet_proportion = MAX(actual_proportion, mte_minimum_proportion)
```

**Example:**
- Actual proportion: 20%
- MTE minimum proportion: 10%
- **Result: 20%** (actual is higher)

---

### Step 5: Check MTE Compliance Status on 1st May 2026

```
was_mte_compliant = (in_scope_compliant_coaches_may_2026 >= minimum_compliant_coaches)
```

**If FALSE**: The operator was NOT compliant with MTE requirements on 1st May 2026. The exemption certificate will be granted but **NOT VALID** until the operator achieves the minimum fleet proportion.

---

### Step 6: Check Current Fleet Compliance

```
current_fleet_proportion = (current_compliant_coaches / current_total_coaches) × 100

meets_minimum_requirement = (current_fleet_proportion >= minimum_fleet_proportion)
```

---

## Complete Calculation Example

### Example 1: Operator Exceeded MTE Requirements

**Input Data:**
```json
{
  "operator_name": "ABC Coaches Ltd",
  "in_scope_compliant_coaches_may_2026": 2,
  "in_scope_total_coaches_may_2026": 5,
  "all_coaches_may_2026": 10,
  "current_compliant_coaches": 3,
  "current_total_coaches": 12
}
```

**Calculation Steps:**

1. **Actual Proportion**: (2 / 10) × 100 = **20%**

2. **MTE Requirement**: 5 in-scope coaches → Band A → 1 compliant coach required

3. **MTE Minimum Proportion**: (1 / 10) × 100 = **10%**

4. **Minimum Fleet Proportion**: MAX(20%, 10%) = **20%**

5. **MTE Compliance Check**: 2 >= 1 → **YES, compliant**

6. **Current Fleet Compliance**: (3 / 12) × 100 = 25% >= 20% → **YES, meets requirement**

**Result:**
- ✅ Exemption certificate is **VALID**
- ✅ Operator must maintain at least **20%** compliant coaches
- ✅ Currently compliant with 25%

---

### Example 2: Operator Did NOT Meet MTE Requirements

**Input Data:**
```json
{
  "operator_name": "XYZ Transport",
  "in_scope_compliant_coaches_may_2026": 4,
  "in_scope_total_coaches_may_2026": 20,
  "all_coaches_may_2026": 40,
  "current_compliant_coaches": 4,
  "current_total_coaches": 40
}
```

**Calculation Steps:**

1. **Actual Proportion**: (4 / 40) × 100 = **10%**

2. **MTE Requirement**: 20 in-scope coaches → Band C → 25% of 20 = 5 compliant coaches required

3. **MTE Minimum Proportion**: (5 / 40) × 100 = **12.5%**

4. **Minimum Fleet Proportion**: MAX(10%, 12.5%) = **12.5%**

5. **MTE Compliance Check**: 4 < 5 → **NO, not compliant**

6. **Current Fleet Compliance**: (4 / 40) × 100 = 10% < 12.5% → **NO, does not meet requirement**

**Result:**
- ⚠️ Exemption certificate is **GRANTED BUT NOT VALID**
- ⚠️ Certificate cannot be used until operator achieves **12.5%** compliant coaches
- ❌ Currently at 10%, needs at least 5 compliant coaches (currently has 4)
- ❌ Cannot provide home-to-school services with non-compliant vehicles until threshold is met

---

## MTE Band Reference Table

| Band | In-Scope Coaches (HTS/RR) | Minimum Compliant Required | Calculation Method |
|------|---------------------------|----------------------------|-------------------|
| **A** | 1 – 5 | 1 coach | Fixed number |
| **B** | 6 – 9 | 2 coaches | Fixed number |
| **C** | 10 – 29 | 25% of in-scope fleet | Percentage (round up) |
| **D** | 30+ | 35% of in-scope fleet | Percentage (round up) |

---

## Generative Prompt Template

```
You are a PSVAR exemption calculator. Given the following operator data, calculate the minimum fleet proportion required for exemption eligibility.

**Operator Data:**
- Operator Name: {operator_name}
- In-scope compliant coaches (1st May 2026): {in_scope_compliant_coaches_may_2026}
- In-scope total coaches (1st May 2026): {in_scope_total_coaches_may_2026}
- All coaches (1st May 2026): {all_coaches_may_2026}
- Current compliant coaches: {current_compliant_coaches}
- Current total coaches: {current_total_coaches}

**Calculate:**

1. Actual in-scope compliant proportion on 1st May 2026
2. MTE band based on in-scope total coaches
3. Minimum compliant coaches required by MTE
4. MTE minimum proportion
5. Final minimum fleet proportion (higher of #1 or #4)
6. Whether operator was MTE-compliant on 1st May 2026
7. Current fleet compliance percentage
8. Whether operator currently meets the minimum requirement

**Provide:**
- All calculation steps with formulas
- Clear explanation of which value was selected and why
- MTE compliance status on 1st May 2026
- Current compliance status
- Certificate validity status
- Any warnings or conditions

**Format output as:**
- Calculation breakdown
- Final minimum fleet proportion percentage
- Certificate status (VALID / GRANTED BUT NOT VALID)
- Compliance summary
```

---

## Validation Rules

Before performing calculations, validate:

1. ✅ `all_coaches_may_2026 > 0` (must have at least one coach)
2. ✅ `in_scope_compliant_coaches_may_2026 >= 0` (cannot be negative)
3. ✅ `in_scope_total_coaches_may_2026 >= 0` (cannot be negative)
4. ✅ `in_scope_compliant_coaches_may_2026 <= in_scope_total_coaches_may_2026` (compliant cannot exceed total in-scope)
5. ✅ `in_scope_total_coaches_may_2026 <= all_coaches_may_2026` (in-scope cannot exceed all coaches)
6. ✅ `current_compliant_coaches >= 0` (cannot be negative)
7. ✅ `current_total_coaches > 0` (must have at least one coach)
8. ✅ `current_compliant_coaches <= current_total_coaches` (compliant cannot exceed total)

---

## Key Definitions

### PSVAR Compliant Coach
A coach that complies with **all paragraphs** of Schedules 1 and 3 of PSVAR:
- **Schedule 1**: Facilities for wheelchair users
- **Schedule 3**: Other accessibility features

### In-Scope Services
- **Home-to-School (HTS)** services
- **Rail Replacement (RR)** services
- Excludes: HTS services with no paying customers

### All Coaches
Total fleet including coaches used for:
- HTS services
- RR services
- Private hire
- Touring
- Any other service

### Partially Compliant
A vehicle that complies with PSVAR Schedule 3, paragraphs 2-5 (excluding certain step requirements) but not fully compliant with all requirements.

---

## Output Format for Generative AI

```json
{
  "calculation_summary": {
    "actual_proportion": "20.0%",
    "mte_band": "A",
    "mte_minimum_coaches": 1,
    "mte_minimum_proportion": "10.0%",
    "minimum_fleet_proportion": "20.0%",
    "calculation_method": "Actual proportion (higher)"
  },
  "mte_compliance_may_2026": {
    "was_compliant": true,
    "required_coaches": 1,
    "actual_coaches": 2,
    "status": "Exceeded MTE requirements"
  },
  "current_compliance": {
    "current_proportion": "25.0%",
    "meets_minimum": true,
    "compliant_coaches": 3,
    "total_coaches": 12,
    "status": "Currently compliant"
  },
  "certificate_status": {
    "is_valid": true,
    "validity_condition": "Certificate is valid immediately",
    "minimum_to_maintain": "20.0%"
  },
  "rationale": [
    "Operator had 2 compliant coaches out of 5 in-scope coaches on 1st May 2026",
    "This represents 20% of their total fleet of 10 coaches",
    "MTE requirement for 5 in-scope coaches was 1 compliant coach (Band A)",
    "MTE minimum proportion would be 10% (1/10)",
    "Actual proportion of 20% is higher than MTE minimum of 10%",
    "Therefore, minimum fleet proportion is 20%",
    "Operator exceeded MTE requirements on 1st May 2026",
    "Current fleet has 3 compliant coaches out of 12 (25%)",
    "Current compliance of 25% exceeds minimum requirement of 20%",
    "Certificate is VALID and operator is currently compliant"
  ]
}
```

---

## Implementation Notes

1. **Always use the HIGHER value** between actual proportion and MTE minimum proportion
2. **Always round UP** when calculating percentages that result in fractional coaches
3. **Check MTE compliance** on 1st May 2026 to determine certificate validity
4. **Compare current compliance** against the calculated minimum to determine ongoing eligibility
5. **Provide clear warnings** if certificate is granted but not valid due to non-compliance

---

*Document Version: 1.0*  
*Based on: Draft exemption terms including minimum fleet calculation (Redacted PDF)*  
*Reference Date: 1st May 2026*