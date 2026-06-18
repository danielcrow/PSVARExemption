#!/usr/bin/env bash

echo "=========================================="
echo "PSVAR Form Filler Agent Import"
echo "=========================================="
echo ""
echo "This script imports the form-filling agent with interactive forms."
echo ""

# Import Python tools first
echo "Step 1: Importing Python tools..."
orchestrate tools import -k python -f tools/evaluate_psvar_exemption.py
orchestrate tools import -k python -f tools/create_certificate_from_assessment.py

if [ $? -eq 0 ]; then
    echo "✓ Python tools imported successfully"
else
    echo "✗ Failed to import Python tools"
    exit 1
fi

echo ""
echo "Step 2: Importing form flow tools..."
orchestrate tools import -k flow -f tools/collect_company_contact_info_flow.py
orchestrate tools import -k flow -f tools/collect_service_confirmation_flow.py
orchestrate tools import -k flow -f tools/collect_fleet_composition_flow.py
orchestrate tools import -k flow -f tools/collect_vehicle_vins_flow.py
orchestrate tools import -k flow -f tools/collect_operational_commitments_flow.py

if [ $? -eq 0 ]; then
    echo "✓ Form flow tools imported successfully"
else
    echo "✗ Failed to import form flow tools"
    exit 1
fi

echo ""
echo "Step 3: Importing form filler agent..."
orchestrate agents import -f agents/psvar_form_filler_agent.yaml

if [ $? -eq 0 ]; then
    echo "✓ Form filler agent imported successfully"
else
    echo "✗ Failed to import form filler agent"
    exit 1
fi

echo ""
echo "=========================================="
echo "Import Complete!"
echo "=========================================="
echo ""
echo "The form filler agent has been imported with:"
echo "  - Interactive form-based data collection"
echo "  - 5 section-specific form flows"
echo "  - Corrected 'paying customers' logic"
echo "  - Automatic data validation"
echo "  - Certificate generation capability"
echo ""
echo "To start using the agent:"
echo "  orchestrate chat start"
echo "  Then select: psvar_form_filler_agent"
echo ""
echo "Key Features:"
echo "  ✓ Interactive forms for each section"
echo "  ✓ Automatic validation in forms"
echo "  ✓ Step-by-step guided workflow"
echo "  ✓ Clear results and next steps"
echo "  ✓ Generates exemption certificates when eligible"
echo ""
echo "Form Tools Available:"
echo "  1. collect_company_contact_info - Company & Contact Information"
echo "  2. collect_service_confirmation - Service Confirmation"
echo "  3. collect_fleet_composition - Fleet Composition"
echo "  4. collect_vehicle_vins - Vehicle VINs"
echo "  5. collect_operational_commitments - Operational Commitments"
echo ""

# Made with Bob
