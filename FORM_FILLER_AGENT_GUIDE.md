# PSVAR Form Filler Agent Guide

## Overview

The **PSVAR Form Filler Agent** is an interactive assistant that guides operators through the PSVAR exemption application process step-by-step. It collects all required information, validates data, and provides immediate assessment results.

## Key Features

✅ **Step-by-Step Guidance** - Walks users through each section of the application  
✅ **Smart Conditional Logic** - Skips irrelevant questions based on responses  
✅ **Real-Time Validation** - Checks data format and consistency as you go  
✅ **Corrected Logic** - Uses the fixed "paying customers" assessment rules  
✅ **Certificate Generation** - Automatically creates exemption certificates when eligible  
✅ **Clear Results** - Provides detailed rationale and next actions  

---

## Installation

Run the import script:

```bash
./import-form-filler-agent.sh
```

This will import:
1. The corrected evaluation tool
2. The certificate generation tool
3. The form filler agent

---

## How to Use

### Starting the Agent

```bash
orchestrate chat start
```

Then select: **psvar_form_filler_agent**

### Conversation Flow

The agent will guide you through 8 sections:

#### 1. Company Information
- Company name
- Operator licence number
- Contact details (name, phone, email)
- Postal address and postcode

#### 2. Service Confirmation
- Service type (HTS = Home-to-School)
- Is it closed-door? (pre-booked, not public)
- Do you have paying customers?

**Critical Logic:**
- ✅ **Free, closed-door HTS** = IN SCOPE for exemption
- ❌ **Paid services** = OUT OF SCOPE (must comply with PSVAR)

#### 3. Fleet Composition
- Total vehicles in HTS fleet
- Fully compliant count
- Partially compliant count
- Non-compliant count

**Validation:** Counts must add up to total fleet size

#### 4. Vehicle Identification Numbers (VINs)
- VINs for all vehicles (17 characters each)
- VINs for partially compliant vehicles (if any)
- VINs for non-compliant vehicles (if any)

**Validation:** 
- Must be exactly 17 characters
- Cannot contain I, O, or Q
- No duplicates allowed

#### 5. Existing Exemption Certificate
- Do you have a current certificate?
- If YES: start date, end date, reference number
- If NO: skip to Section 7

#### 6. Operational Conditions (Only if has certificate)
- Certificate carried onboard?
- Alternative accessible transport available?
- Written confirmation retained?

#### 7. Band Compliance Requirements
- Have you read your band requirements?

**Bands by Fleet Size:**
- Band A: 1-5 vehicles
- Band B: 6-9 vehicles
- Band C: 10-29 vehicles
- Band D: 30+ vehicles

#### 8. Fleet Changes (Only if has certificate)
- Has fleet size changed?
- If YES: Was DfT notified within 5 days?

---

## Assessment Outcomes

### ✅ CAN_HAVE_EXEMPTION
**Meaning:** Eligible for PSVAR exemption

**What Happens:**
- Certificate is generated (if applicable)
- Compliance band is assigned
- Requirements are explained
- Next steps provided

**Example:**
```
✅ Congratulations! You are eligible for a PSVAR exemption.

Compliance Band: C (10-29 vehicles)
Current Milestone: 50% fully compliant (met ✓)

Rationale:
- Fleet meets Band C milestone requirements
- All operational commitments confirmed
- VINs validated successfully

Next Actions:
- Carry exemption certificate onboard
- Maintain minimum compliance percentage
- Notify DfT of any fleet size changes
```

---

### ❌ CANNOT_HAVE_EXEMPTION
**Meaning:** Does not meet exemption criteria

**What Happens:**
- Specific reasons explained
- Requirements outlined
- Steps to become eligible provided

**Example:**
```
❌ Your application cannot be approved at this time.

Rationale:
- Fleet has only 20% fully compliant vehicles
- Band C requires 50% fully compliant
- Below minimum milestone requirements

Next Actions:
- Increase compliant vehicles to at least 50%
- Reapply once milestone is met
- Consider upgrading existing vehicles
```

---

### ⚠️ FURTHER_INVESTIGATION_REQUIRED
**Meaning:** DVSA review needed

**What Happens:**
- Issues identified
- DVSA task created
- Additional information requested

**Example:**
```
⚠️ Your application requires DVSA review.

Issues Identified:
- VIN ABC123456789INVALID has invalid format
- Fleet size mismatch (stated 10, counted 8)
- Duplicate VIN detected: 1HGBH41JXMN109186

Next Actions:
- Correct invalid VINs
- Reconcile fleet counts
- DVSA will contact you for clarification
```

---

### ℹ️ OUT_OF_SCOPE
**Meaning:** Service doesn't qualify for exemption assessment

**What Happens:**
- Scope rules explained
- PSVAR compliance requirements provided

**Example:**
```
ℹ️ Your service is outside the scope of this exemption.

Reason:
- HTS services with paying customers are considered 
  public service vehicles
- Public service vehicles must comply with PSVAR 
  without exemption

Guidance:
- Review PSVAR Schedules 1 and 3 requirements
- Ensure all vehicles meet accessibility standards
- Contact DVSA for compliance support
```

---

### 🎉 EXEMPTION_NOT_REQUIRED
**Meaning:** Entire fleet is fully compliant

**What Happens:**
- Congratulations message
- Encouragement to maintain compliance

**Example:**
```
🎉 Excellent news! Your entire fleet is fully PSVAR compliant.

You do not need an exemption because all 12 vehicles 
in your HTS fleet meet PSVAR requirements.

Recommendation:
- Continue maintaining full compliance
- Keep vehicle accessibility features in good condition
- No further action required
```

---

## Data Validation Rules

### VIN Format
- **Length:** Exactly 17 characters
- **Characters:** Letters (A-Z) and numbers (0-9)
- **Excluded:** I, O, Q (easily confused with 1, 0)
- **Uniqueness:** No duplicates allowed

**Valid Examples:**
```
1HGBH41JXMN109186
2FMDK3GC3BBB12345
3FADP4BJ3BM123456
```

**Invalid Examples:**
```
ABC123 (too short)
1HGBH41JXMN109186O (contains O)
1HGBH41JXMN109186 (duplicate if used twice)
```

### Fleet Size Consistency
```
Total Fleet Size = Fully Compliant + Partially Compliant + Non-Compliant
```

**Example:**
- Total: 10 vehicles
- Fully compliant: 6
- Partially compliant: 2
- Non-compliant: 2
- ✅ Valid (6 + 2 + 2 = 10)

**Invalid Example:**
- Total: 10 vehicles
- Fully compliant: 5
- Partially compliant: 2
- Non-compliant: 2
- ❌ Invalid (5 + 2 + 2 = 9, not 10)

### Date Format
All dates must be in **YYYY-MM-DD** format:
- ✅ Valid: `2026-01-15`
- ❌ Invalid: `15/01/2026`, `Jan 15 2026`

---

## Service Scope Rules (CRITICAL)

### IN SCOPE for Exemption Assessment

✅ **Home-to-School (HTS) services that are:**
- Closed-door (pre-booked, not available to general public)
- **WITHOUT paying customers** (free services)

**Why:** Free, closed-door services are treated as private hire/contract services and may qualify for exemptions.

### OUT OF SCOPE (Must Comply with PSVAR)

❌ **Services that are:**
- HTS with paying customers (public service vehicles)
- Not closed-door (available to general public)
- Not home-to-school or rail replacement

**Why:** Paid services are public service vehicles and must comply with PSVAR without exemption.

---

## Compliance Bands and Requirements (2026)

| Band | Fleet Size | Minimum Fully Compliant |
|------|------------|------------------------|
| A    | 1-5        | 50%                    |
| B    | 6-9        | 50%                    |
| C    | 10-29      | 50%                    |
| D    | 30+        | 50%                    |

**Note:** Requirements increase over time according to PSVAR regulations.

---

## Tips for Success

### Before Starting
1. ✅ Gather all company information
2. ✅ Have VINs ready for all vehicles
3. ✅ Know your fleet composition
4. ✅ Have existing certificate details (if applicable)

### During the Process
1. ✅ Answer questions accurately
2. ✅ Double-check VIN format
3. ✅ Verify fleet counts add up
4. ✅ Review summary before submitting

### After Assessment
1. ✅ Save any generated certificates
2. ✅ Follow all next actions
3. ✅ Keep records of assessment
4. ✅ Notify DfT of fleet changes

---

## Common Issues and Solutions

### Issue: "OUT_OF_SCOPE - Paying Customers"
**Problem:** Service has paying customers  
**Solution:** Paid HTS services must comply with PSVAR without exemption. Review PSVAR requirements and ensure all vehicles meet accessibility standards.

### Issue: "Invalid VIN Format"
**Problem:** VIN doesn't meet format requirements  
**Solution:** Check VIN is exactly 17 characters and doesn't contain I, O, or Q. Verify against vehicle documentation.

### Issue: "Fleet Size Mismatch"
**Problem:** Counts don't add up to total  
**Solution:** Recount vehicles in each category. Ensure: Total = Fully + Partially + Non-compliant.

### Issue: "Below Milestone Requirements"
**Problem:** Not enough compliant vehicles for band  
**Solution:** Increase compliant vehicles to meet band requirements before reapplying.

---

## Comparison with Other Agents

| Feature | Form Filler Agent | Complete Assessment Agent |
|---------|------------------|--------------------------|
| **Interaction Style** | Step-by-step form | Conversational |
| **Data Collection** | Structured sections | Flexible order |
| **Validation** | Real-time | End of collection |
| **Best For** | First-time users | Experienced users |
| **Certificate Generation** | Automatic | On request |

---

## Support and Contact

For technical issues with the agent:
- Check validation messages
- Review this guide
- Ensure all required fields provided

For PSVAR policy questions:
- Contact Department for Transport (DfT)
- Reference your operator licence number
- Include assessment date

For DVSA enforcement queries:
- Contact DVSA directly
- Provide certificate reference (if applicable)
- Include vehicle VINs

---

## Version History

- **v1.0** (2026-06-08)
  - Initial release
  - Corrected "paying customers" logic
  - Step-by-step form guidance
  - Real-time validation
  - Certificate generation

---

## Related Documentation

- [`PSVAR_DEMO_DATA_ALL_OUTCOMES.md`](PSVAR_DEMO_DATA_ALL_OUTCOMES.md) - Test scenarios
- [`SCHEDULE_A_CALCULATION.md`](SCHEDULE_A_CALCULATION.md) - Calculation details
- [`Fw_ Draft exemption terms including minimum fleet calculation_Redacted.pdf`](Fw_%20Draft%20exemption%20terms%20including%20minimum%20fleet%20calculation_Redacted.pdf) - Official guidance

---

**Made with Bob** 🤖