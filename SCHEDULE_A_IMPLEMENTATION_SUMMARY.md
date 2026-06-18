# Schedule A Implementation Summary

## Overview

This document summarizes the implementation of the Schedule A minimum fleet proportion calculation for PSVAR exemption assessments, as specified in the draft exemption terms from the Secretary of State.

**Implementation Date**: 2026-06-04  
**Status**: ✅ Complete

---

## What Was Implemented

### 1. New Input Fields

Added two new optional fields to [`PSVARAssessmentInput`](tools/evaluate_psvar_exemption.py):

```python
in_scope_compliant_coaches_may_2026: Optional[int]
    # Total number of fully PSVAR compliant coaches used on 1st May 2026
    # to provide home to school and rail replacement services combined

all_coaches_may_2026: Optional[int]
    # Total number of coaches used on 1st May 2026 to provide any service
    # (including HTS, RR, private hire, touring, etc)
```

### 2. Calculation Function

Created [`_calculate_minimum_fleet_proportion()`](tools/evaluate_psvar_exemption.py#L417-L497) function that:

- Calculates actual in-scope compliant proportion: `(InScopeCompliantCoaches / AllCoaches) × 100`
- Determines MTE minimum requirements based on in-scope coach count
- Calculates MTE minimum proportion: `(MinimumCompliantCoaches / AllCoaches) × 100`
- Returns the **higher** of the two percentages
- Provides detailed rationale for the calculation
- Warns if operator was non-compliant with MTE on 1st May 2026

### 3. MTE Requirements Table

Implemented the Medium Term Exemption requirements:

| In-Scope Coaches | Minimum Compliant Required |
|------------------|----------------------------|
| 1-5 | 1 coach |
| 6-9 | 2 coaches |
| 10-29 | 25% (rounded up) |
| 30+ | 35% (rounded up) |

### 4. Integration into Evaluation Logic

Updated [`evaluate_psvar_exemption()`](tools/evaluate_psvar_exemption.py#L789-835) to:

- Validate the May 2026 input data
- Call the calculation function when data is provided
- Add calculation results to the assessment rationale
- Compare current fleet compliance against minimum proportion
- Handle missing or incomplete data appropriately

### 5. Validation Rules

Implemented comprehensive validation:

- ✅ Both fields must be provided together (or both omitted)
- ✅ `all_coaches_may_2026` must be greater than zero
- ✅ `in_scope_compliant_coaches_may_2026` cannot be negative
- ✅ In-scope compliant coaches cannot exceed total coaches

### 6. Comprehensive Testing

Created [`tests/test_schedule_a_calculation.py`](tests/test_schedule_a_calculation.py) with:

- ✅ Both examples from the draft exemption text
- ✅ All MTE bands (A, B, C, D) with various fleet sizes
- ✅ Edge cases (zero coaches, boundary values)
- ✅ Scenarios where actual > MTE and MTE > actual
- ✅ Non-compliance warning verification
- **Total**: 15+ comprehensive test cases

### 7. Documentation

Created comprehensive documentation:

- ✅ [`SCHEDULE_A_CALCULATION.md`](SCHEDULE_A_CALCULATION.md) - Complete technical documentation
- ✅ [`SCHEDULE_A_IMPLEMENTATION_SUMMARY.md`](SCHEDULE_A_IMPLEMENTATION_SUMMARY.md) - This file
- ✅ Updated [`README.md`](README.md) with Schedule A overview

---

## How It Works

### Example 1: Operator Exceeded MTE Requirements

**Input:**
- In-scope compliant coaches (May 2026): 2
- All coaches (May 2026): 10
- In-scope coaches on May 2026: 5 (requires 1 compliant per MTE)

**Calculation:**
1. Actual: (2 / 10) × 100 = **20%**
2. MTE: (1 / 10) × 100 = **10%**
3. **Result: 20%** ← Higher value used

**Outcome:** Exemption valid immediately. Operator must maintain ≥20% compliance.

### Example 2: Operator Did Not Meet MTE Requirements

**Input:**
- In-scope compliant coaches (May 2026): 4
- All coaches (May 2026): 40
- In-scope coaches on May 2026: 20 (requires 5 compliant per MTE)

**Calculation:**
1. Actual: (4 / 40) × 100 = **10%**
2. MTE: (5 / 40) × 100 = **12.5%**
3. **Result: 12.5%** ← Higher value used

**Outcome:** Exemption granted but **NOT VALID** until operator achieves ≥12.5% compliance. Cannot be used for HTS services until threshold met.

---

## Files Modified

### Core Implementation
- ✅ [`tools/evaluate_psvar_exemption.py`](tools/evaluate_psvar_exemption.py)
  - Added input fields (lines 91-98)
  - Added calculation function (lines 417-497)
  - Integrated into evaluation logic (lines 789-835)

### Testing
- ✅ [`tests/test_schedule_a_calculation.py`](tests/test_schedule_a_calculation.py) - New file with 15+ tests

### Documentation
- ✅ [`SCHEDULE_A_CALCULATION.md`](SCHEDULE_A_CALCULATION.md) - New comprehensive guide
- ✅ [`SCHEDULE_A_IMPLEMENTATION_SUMMARY.md`](SCHEDULE_A_IMPLEMENTATION_SUMMARY.md) - This file
- ✅ [`README.md`](README.md) - Updated with Schedule A overview

---

## Key Features

### 1. Automatic Calculation
When May 2026 data is provided, the system automatically:
- Calculates both proportions
- Selects the higher value
- Validates MTE compliance
- Provides detailed rationale

### 2. Detailed Rationale
The assessment output includes:
- Actual in-scope compliant proportion
- MTE requirement for the fleet size
- MTE minimum proportion
- Which method was used (higher value)
- Warning if non-compliant with MTE
- Current fleet comparison

### 3. Flexible Usage
The May 2026 fields are **optional**:
- If provided: Schedule A calculation is performed
- If omitted: Assessment proceeds without Schedule A calculation
- Partial data: System requests missing information

### 4. MTE Compliance Warning
If operator was non-compliant with MTE on 1st May 2026:
- ⚠️ Warning issued in rationale
- 📋 Exemption granted but marked as "not valid"
- 🚫 Cannot be used for HTS services until threshold met
- ✅ Must achieve minimum proportion first

---

## Usage

### For Operators Applying for Exemption

When completing the assessment, provide:
1. Your fleet composition on **1st May 2026**:
   - How many compliant coaches were used for HTS/RR services?
   - How many total coaches did you operate (all services)?

2. The system will calculate your minimum fleet proportion

3. You'll receive clear guidance on:
   - Your required minimum percentage
   - Whether you met MTE requirements
   - Current compliance status
   - Next steps

### For DVSA Officers

The assessment output includes:
- Complete Schedule A calculation breakdown
- MTE compliance status on 1st May 2026
- Current fleet compliance comparison
- Clear rationale for exemption validity

---

## Testing

Run the comprehensive test suite:

```bash
pytest tests/test_schedule_a_calculation.py -v
```

Tests cover:
- ✅ Both examples from draft exemption text
- ✅ All MTE bands (A, B, C, D)
- ✅ Edge cases and boundary conditions
- ✅ Validation rules
- ✅ Non-compliance warnings

---

## References

- **Source Document**: Draft exemption terms from Secretary of State
- **Legal Basis**: Section 178, Equality Act 2010
- **Schedule**: Schedule A - Calculation of Minimum fleet proportion
- **MTE Requirements**: Medium Term Exemption scheme table

---

## Next Steps

### Optional Enhancements

1. **Data Collection Tools**: Update intake forms to collect May 2026 data
2. **Historical Tracking**: Store May 2026 data for audit purposes
3. **Reporting**: Generate Schedule A compliance reports
4. **Monitoring**: Track operators' ongoing compliance with minimum proportion

### Integration Points

- ✅ Evaluation tool: Complete
- ⏳ Intake agent: May need updates to collect May 2026 data
- ⏳ Email notifications: Already includes rationale
- ⏳ DVSA review workflow: Can access full calculation details

---

## Compliance

This implementation fully complies with:
- ✅ Schedule A calculation methodology
- ✅ MTE requirements table
- ✅ Rounding rules (always round up)
- ✅ Higher-of-two-values selection
- ✅ Non-compliance warning requirements

---

*Implementation completed: 2026-06-04*  
*All requirements from Schedule A have been successfully implemented and tested.*