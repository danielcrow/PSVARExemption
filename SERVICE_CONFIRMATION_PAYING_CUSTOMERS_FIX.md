
## Problem
When users checked "This service has NO paying customers" in the form, the system was incorrectly evaluating the service as OUT OF SCOPE (as if it HAD paying customers).

## Root Cause

### The Inversion Issue
There was a **field name mismatch** between the form flow and the evaluation tool:

**Form Flow Output** (`collect_service_confirmation_flow.py`):
- Field: `has_no_paying_customers`
- Meaning: `True` = NO paying customers (IN SCOPE)
- Meaning: `False` = HAS paying customers (OUT OF SCOPE)

**Evaluation Tool Input** (`evaluate_psvar_exemption.py`):
- Field: `hts_has_paying_customers`
- Meaning: `True` = HAS paying customers (OUT OF SCOPE)
- Meaning: `False` = NO paying customers (IN SCOPE)

**These are inverted!** When the form returned `has_no_paying_customers=True`, the evaluation tool was receiving it as `hts_has_paying_customers=True`, which means the opposite.

### Evaluation Logic (Line 665 in evaluate_psvar_exemption.py)
```python
elif service_types == {"HTS"} and assessment.hts_has_paying_customers is True:
    rationale.append("HTS services with paying customers are outside this exemption guidance scope...")
    final_case_outcome = "OUT_OF_SCOPE"
```

This checks if `hts_has_paying_customers is True` to mark as OUT OF SCOPE.

## Solution Applied

### 1. Changed Form Flow Output Schema
Updated `ServiceConfirmationOutput` in `collect_service_confirmation_flow.py`:

**Before:**
```python
has_no_paying_customers: bool = Field(
    description="Whether there are NO paying customers (true means no paying customers)"
)
```

**After:**
```python
has_paying_customers: bool = Field(
    description="Whether there ARE paying customers (true means has paying customers, false means no paying customers)"
)
```

### 2. Updated Form Field and Logic
**Form field name changed:**
- From: `has_no_paying_customers`
- To: `has_no_paying_customers_checkbox` (internal form field)

**Added inversion logic in output mapping:**
```python
# Checkbox checked (True) = NO paying customers = has_paying_customers should be False
# Checkbox unchecked (False) = HAS paying customers = has_paying_customers should be True
aflow.map_output(
    output_variable="has_paying_customers",
    expression="not bool(flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers_checkbox)"
)
```

**Updated form label for clarity:**
```python
service_form.boolean_input_field(
    name="has_no_paying_customers_checkbox",
    label="✓ This service has NO paying customers (free service)"
)
```

### 3. Maintained Correct In-Scope Logic
The `is_in_scope` calculation still uses the checkbox directly (not inverted):
```python
aflow.map_output(
    output_variable="is_in_scope",
    expression="bool(...is_hts_service) and bool(...is_closed_door) and bool(...has_no_paying_customers_checkbox)"
)
```

This is correct because:
- Checkbox checked = NO paying customers = IN SCOPE ✓
- The `is_in_scope` field is for display/validation only
- The `has_paying_customers` field (inverted) is what gets passed to the evaluation tool

## How It Works Now

### User Interaction
1. User sees form with checkbox: "✓ This service has NO paying customers (free service)"
2. User checks the box (meaning: we have NO paying customers)

### Data Flow
1. Form field `has_no_paying_customers_checkbox` = `True`
2. Output `has_paying_customers` = `not True` = `False`
3. Output `is_in_scope` = `True` (because checkbox is checked)
4. Evaluation tool receives `hts_has_paying_customers=False`
5. Evaluation tool correctly identifies service as IN SCOPE ✓

### Correct Outcomes

| User Checks Box | Checkbox Value | has_paying_customers | is_in_scope | Evaluation Result |
|----------------|----------------|---------------------|-------------|-------------------|
| ✓ (NO paying)  | True           | False               | True        | IN SCOPE ✓        |
| ✗ (HAS paying) | False          | True                | False       | OUT OF SCOPE ✓    |

## Testing

To verify the fix:

```bash
# Re-import the fixed flow
orchestrate tools import -k flow -f tools/collect_service_confirmation_flow.py

# Test with the agent
orchestrate chat start
# Select: psvar_form_filler_agent

# In the form:
# 1. Check "This is a home-to-school (HTS) service"
# 2. Check "This is a closed-door service"
# 3. Check "This service has NO paying customers (free service)"
# 4. Submit form

# Expected: Service should be IN SCOPE and proceed to fleet composition
```

## Files Modified

1. `tools/collect_service_confirmation_flow.py`
   - Changed output field from `has_no_paying_customers` to `has_paying_customers`
   - Added inversion logic: `not bool(checkbox_value)`
   - Updated form field label for clarity
   - Maintained correct `is_in_scope` calculation

## Related Files

- `tools/evaluate_psvar_exemption.py` - Expects `hts_has_paying_customers` field (no changes needed)
- `agents/psvar_form_filler_agent.yaml` - Uses the form flow (no changes needed)

## Key Takeaway

When integrating forms with evaluation logic, ensure field names and their boolean meanings are **consistent** across all components. A field named `has_X` should mean the same thing everywhere - either "has X" or "doesn't have X", but not both!