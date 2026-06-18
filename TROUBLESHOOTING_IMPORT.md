# Troubleshooting Agent Import Issues

## Common Errors and Solutions

### Error: "kid not found in response" (Status 500)

**Error Message:**
```
ClientAPIException(status_code=500, message={"message":"wxo error: MCSP - kid not found in response","code":500})
```

**Cause:** Authentication token issue with watsonx Orchestrate API

**Solutions:**

#### 1. Re-authenticate to watsonx Orchestrate

```bash
# Activate the environment again
orchestrate env activate emea-1

# You'll be prompted for credentials
# Enter your username and password
```

#### 2. Check Environment Status

```bash
# List available environments
orchestrate env list

# Check current active environment
orchestrate env show
```

#### 3. Try Manual Import (One at a Time)

Instead of using the script, import each component manually:

```bash
# Step 1: Import evaluation tool
orchestrate tools import -k python -f tools/evaluate_psvar_exemption.py

# Step 2: Import certificate tool
orchestrate tools import -k python -f tools/create_certificate_from_assessment.py

# Step 3: Import agent
orchestrate agents import -f agents/psvar_form_filler_agent_simple.yaml
```

#### 4. Check API Connectivity

```bash
# Test basic connectivity
orchestrate agents list

# If this works, the API is accessible
```

---

### Error: "Failed to decode JSON response" (Status 500)

**Cause:** Agent instructions too long or malformed YAML

**Solution:** Use the simplified agent version

```bash
orchestrate agents import -f agents/psvar_form_filler_agent_simple.yaml
```

---

### Error: "Tool not found"

**Cause:** Required tools not imported before agent

**Solution:** Import tools first, then agent

```bash
# Import tools first
orchestrate tools import -k python -f tools/evaluate_psvar_exemption.py
orchestrate tools import -k python -f tools/create_certificate_from_assessment.py

# Then import agent
orchestrate agents import -f agents/psvar_form_filler_agent_simple.yaml
```

---

## Alternative: Use Existing Complete Assessment Agent

If the form filler agent continues to have issues, you can use the existing complete assessment agent which is already working:

```bash
orchestrate chat start
# Select: psvar_complete_assessment_agent
```

This agent has the same corrected logic and can handle the assessment process.

---

## Verification Steps

After successful import, verify:

### 1. Check Tools Are Imported

```bash
orchestrate tools list | grep -E "(evaluate_psvar|create_certificate)"
```

Expected output:
```
evaluate_psvar_exemption
create_certificate_from_assessment
```

### 2. Check Agent Is Imported

```bash
orchestrate agents list | grep psvar_form_filler
```

Expected output:
```
psvar_form_filler_agent
```

### 3. Test the Agent

```bash
orchestrate chat start
# Select: psvar_form_filler_agent
# Try: "Hello, I need help with a PSVAR exemption"
```

---

## If All Else Fails

### Option 1: Use the Web UI

1. Log into watsonx Orchestrate web interface
2. Navigate to Agents section
3. Manually create agent using the YAML content
4. Import tools via UI

### Option 2: Contact Support

If authentication issues persist:
- Contact IBM watsonx Orchestrate support
- Provide error message and environment details
- Check if your account has proper permissions

### Option 3: Use Alternative Agent

The project has multiple agents that work:

```bash
# List all PSVAR agents
orchestrate agents list | grep psvar

# Available agents:
# - psvar_complete_assessment_agent (already working)
# - psvar_exemption_form_agent (existing form agent)
# - psvar_intake_agent (intake specialist)
```

---

## Environment-Specific Issues

### Local Developer Edition

If using Local Developer Edition:

```bash
# Activate local environment
orchestrate env activate local

# Then import
orchestrate agents import -f agents/psvar_form_filler_agent_simple.yaml
```

### Production Environment

If using production watsonx Orchestrate:

```bash
# Ensure you're on the right environment
orchestrate env activate emea-1

# Check your permissions
orchestrate env show
```

---

## Quick Recovery Steps

If you just need to get working quickly:

1. **Use the existing complete assessment agent** (already imported and working)
   ```bash
   orchestrate chat start
   # Select: psvar_complete_assessment_agent
   ```

2. **Or manually import just the fixed evaluation tool**
   ```bash
   orchestrate tools import -k python -f tools/evaluate_psvar_exemption.py
   ```
   
   Then use it with the existing agents.

---

## Summary of What's Already Working

Even if the new form filler agent won't import, you have:

✅ **Fixed evaluation tool** - Can be imported separately  
✅ **Complete assessment agent** - Already working  
✅ **Certificate generation** - Already available  
✅ **Corrected logic** - In the evaluation tool  

The core functionality is available through existing agents!

---

## Need Help?

1. Check this troubleshooting guide
2. Review error messages carefully
3. Try manual import steps
4. Use existing working agents
5. Contact IBM support if authentication issues persist