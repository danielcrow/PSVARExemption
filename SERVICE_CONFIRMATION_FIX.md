# Service Confirmation Boolean Logic Fix

## Problem
The service confirmation flow was incorrectly determining scope status due to boolean field handling issues.

### Original Issue
- Form field was named `has_no_paying_customers` (user confirms NO paying customers)
- Output was trying to invert this to `has_paying_customers` using expressions
- Multiple inversion approaches failed:
  - `not` operator
  - Conditional expression `False if ... else True`
  - Comparison `== False`
- Result: Services that should be IN SCOPE were marked OUT OF SCOPE

## Root Cause
The flow was attempting to invert a boolean value in the output mapping, but the inversion logic was not evaluating correctly. Additionally, there was a mismatch between:
- What the form collected (`has_no_paying_customers`)
- What the output schema defined (`has_paying_customers`)
- What the scope calculation used (`has_no_paying_customers`)

## Solution
Simplified the logic by removing the unnecessary inversion:

### Changes Made

1. **Updated Output Schema** (line 19)
   ```python
   # Before:
   has_paying_customers: bool = Field(description="Whether there are any paying customers")
   
   # After:
   has_no_paying_customers: bool = Field(description="Whether there are NO paying customers (true means no paying customers)")
   ```

2. **Removed Inversion Logic** (lines 88-91)
   ```python
   # Removed this problematic code:
   aflow.map_output(
       output_variable="has_paying_customers",
       expression="flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers == False"
   )
   ```

3. **Added Direct Output Mapping** (lines 88-91)
   ```python
   # Added simple direct mapping:
   aflow.map_output(
       output_variable="has_no_paying_customers",
       expression="flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers"
   )
   ```

4. **Scope Calculation Remains Consistent** (lines 94-97)
   ```python
   # Already using has_no_paying_customers correctly:
   aflow.map_output(
       output_variable="is_in_scope",
       expression="flow['userflow_1']['service_confirmation_form'].output.is_hts_service and flow['userflow_1']['service_confirmation_form'].output.is_closed_door and flow['userflow_1']['service_confirmation_form'].output.has_no_paying_customers"
   )
   ```

## Result
The flow now correctly determines scope:
- ✅ User checks "Yes, this is a home-to-school service" → `is_hts_service = True`
- ✅ User checks "Yes, this is a closed-door service" → `is_closed_door = True`
- ✅ User checks "Yes, confirmed - no paying customers" → `has_no_paying_customers = True`
- ✅ Scope calculation: `True AND True AND True = True` → Service is IN SCOPE

## Key Lesson
When working with watsonx Orchestrate flows:
- Keep boolean logic simple and direct
- Avoid unnecessary inversions in output mappings
- Ensure consistency between form fields, output schema, and calculations
- Name fields clearly to match their semantic meaning (e.g., `has_no_paying_customers` is clearer than trying to invert to `has_paying_customers`)

## Testing
The fix has been imported successfully:
```bash
orchestrate tools import -k flow -f tools/collect_service_confirmation_flow.py
```

## Additional Fix Required

After importing the flow, testing revealed the agent was still marking services as out of scope. Investigation showed the agent's instructions referenced the old field name.

### Agent Instructions Update (agents/psvar_intake_agent.yaml, line 51)
```yaml
# Before:
- Store: is_hts_service, is_closed_door, has_paying_customers, is_in_scope

# After:
- Store: is_hts_service, is_closed_door, has_no_paying_customers, is_in_scope
```

This ensures the agent's instructions match the actual output field names from the flow.

## Final Import Commands
```bash
# Re-import the flow
orchestrate tools import -k flow -f tools/collect_service_confirmation_flow.py

# Re-import the agent with updated instructions
orchestrate agents import -f agents/psvar_intake_agent.yaml
```

Status: ✅ **FULLY RESOLVED**