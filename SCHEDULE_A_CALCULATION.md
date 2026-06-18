# Schedule A: Minimum Fleet Proportion Calculation

## Overview

This document explains the implementation of the minimum fleet proportion calculation as specified in Schedule A of the draft exemption terms from the Secretary of State.

## Purpose

The minimum fleet proportion calculation determines the percentage of PSVAR compliant coaches that an operator must maintain across their entire coach fleet to be eligible for an exemption certificate.

## Calculation Method

The minimum fleet proportion is calculated as **the higher of two values**:

### Calculation 1: Actual In-Scope Compliant Proportion

```
(InScopeCompliantCoaches / AllCoaches) × 100
```

Where:
- **InScopeCompliantCoaches**: Total number of fully PSVAR compliant coaches used on 1st May 2026 to provide home-to-school (HTS) and rail replacement (RR) services combined
- **AllCoaches**: Total number of coaches used on 1st May 2026 to provide any service (including HTS, RR, private hire, touring, etc.)

### Calculation 2: MTE Minimum Requirements

```
(MinimumCompliantCoaches / AllCoaches) × 100
```

Where **MinimumCompliantCoaches** is determined by the Medium Term Exemption (MTE) requirements based on the number of in-scope coaches on 1st May 2026:

| In-Scope Coaches on 1st May 2026 | Minimum Compliant Coaches Required |
|-----------------------------------|-------------------------------------|
| 1 – 5 coaches | 1 PSVAR compliant coach |
| 6 – 9 coaches | 2 PSVAR compliant coaches |
| 10 – 29 coaches | 25% of HTS/RR coaches (rounded up) |
| 30 or more coaches | 35% of HTS/RR coaches (rounded up) |

### Final Calculation

The **minimum fleet proportion** is the **higher** of Calculation 1 or Calculation 2.

## Examples

### Example 1: Operator Exceeded MTE Requirements

**Scenario:**
- 5 coaches on HTS/RR services on 1st May 2026
- MTE requirement: 1 compliant coach minimum
- Operator had: 2 compliant coaches (exceeded requirement)
- Total fleet: 10 coaches

**Calculation:**
1. Actual proportion: (2 / 10) × 100 = **20%**
2. MTE minimum: (1 / 10) × 100 = **10%**
3. **Result: 20%** (actual is higher)

### Example 2: Operator Did Not Meet MTE Requirements

**Scenario:**
- 20 coaches on HTS/RR services on 1st May 2026
- MTE requirement: 25% of 20 = 5 compliant coaches
- Operator had: 4 compliant coaches (did not meet requirement)
- Total fleet: 40 coaches

**Calculation:**
1. Actual proportion: (4 / 40) × 100 = **10%**
2. MTE minimum: (5 / 40) × 100 = **12.5%**
3. **Result: 12.5%** (MTE minimum is higher)

**Important Note:** In this case, the operator was not compliant with MTE requirements on 1st May 2026. The exemption certificate would be granted but **not valid** until the operator achieves the minimum 12.5% proportion. The certificate cannot be used for home-to-school services until this threshold is met.

## Implementation

### Input Fields

Two new fields have been added to `PSVARAssessmentInput`:

```python
in_scope_compliant_coaches_may_2026: Optional[int]
    # Total number of fully PSVAR compliant coaches used on 1st May 2026
    # to provide home to school and rail replacement services combined

all_coaches_may_2026: Optional[int]
    # Total number of coaches used on 1st May 2026 to provide any service
    # (including HTS, RR, private hire, touring, etc)
```

### Calculation Function

The calculation is implemented in `_calculate_minimum_fleet_proportion()`:

```python
def _calculate_minimum_fleet_proportion(
    in_scope_compliant_coaches: int,
    all_coaches: int,
) -> tuple[float, str, list[str]]:
    """
    Calculate the minimum fleet proportion according to Schedule A.
    
    Returns:
        tuple: (minimum_percentage, calculation_method, rationale_items)
    """
```

### Integration

The calculation is integrated into the main `evaluate_psvar_exemption()` function and:

1. Validates the input data
2. Calculates both proportions
3. Selects the higher value
4. Checks if the operator was MTE-compliant on 1st May 2026
5. Compares current fleet compliance against the minimum proportion
6. Adds detailed rationale explaining the calculation

## Validation Rules

The implementation includes the following validations:

1. **Both fields required**: If one field is provided, both must be provided
2. **Positive values**: `all_coaches_may_2026` must be greater than zero
3. **Non-negative**: `in_scope_compliant_coaches_may_2026` cannot be negative
4. **Logical constraint**: In-scope compliant coaches cannot exceed total coaches

## Rationale Output

The calculation provides detailed rationale including:

- Actual in-scope compliant proportion
- MTE requirement for the number of in-scope coaches
- MTE minimum proportion
- Which calculation method was used (higher value)
- Warning if operator was non-compliant with MTE on 1st May 2026
- Comparison of current fleet compliance vs. minimum proportion

## Impact on Exemption Eligibility

### If Operator Met MTE Requirements on 1st May 2026

The exemption certificate is valid immediately, and the operator must maintain at least the calculated minimum fleet proportion.

### If Operator Did NOT Meet MTE Requirements on 1st May 2026

The exemption certificate is granted but **not valid** until the operator achieves the minimum percentage. The certificate **cannot be used** to provide home-to-school services using non-compliant vehicles until the minimum proportion is achieved.

## Testing

Comprehensive tests are provided in `tests/test_schedule_a_calculation.py` covering:

- Both examples from the draft exemption text
- All MTE bands (A, B, C, D)
- Edge cases (zero coaches, boundary values)
- Scenarios where actual > MTE and MTE > actual
- Non-compliance warnings

## References

- Draft exemption text from Secretary of State (Section 178, Equality Act 2010)
- Schedule A: Calculation of Minimum fleet proportion
- Medium Term Exemption (MTE) requirements table

---

*Implementation Date: 2026-06-04*  
*Based on: Draft exemption terms including minimum fleet calculation*