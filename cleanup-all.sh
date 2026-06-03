#!/usr/bin/env bash

set -euo pipefail

echo "=========================================="
echo "Cleaning watsonx Orchestrate Environment"
echo "=========================================="
echo ""

# Remove all agents
echo "Removing agents..."
orchestrate agents remove -n psvar_intake_agent -k native 2>/dev/null || echo "  - psvar_intake_agent not found (skipping)"
orchestrate agents remove -n psvar_exemption_assessment -k native 2>/dev/null || echo "  - psvar_exemption_assessment not found (skipping)"
orchestrate agents remove -n psvar_exemption_assessor -k native 2>/dev/null || echo "  - psvar_exemption_assessor not found (skipping)"
orchestrate agents remove -n psvar_exemption_form_agent -k native 2>/dev/null || echo "  - psvar_exemption_form_agent not found (skipping)"
orchestrate agents remove -n dvsa_form_agent -k native 2>/dev/null || echo "  - dvsa_form_agent not found (skipping)"
orchestrate agents remove -n Test_Agent_5254kO -k native 2>/dev/null || echo "  - Test_Agent_5254kO not found (skipping)"
orchestrate agents remove -n AskOrchestrate -k native 2>/dev/null || echo "  - AskOrchestrate not found (skipping)"
echo "✓ Agents removed"
echo ""

# Remove all tools
echo "Removing tools..."
orchestrate tools remove -n evaluate_psvar_exemption 2>/dev/null || echo "  - evaluate_psvar_exemption not found (skipping)"
orchestrate tools remove -n send_assessment_outcome_email 2>/dev/null || echo "  - send_assessment_outcome_email not found (skipping)"
orchestrate tools remove -n psvar_exemption_form_tool 2>/dev/null || echo "  - psvar_exemption_form_tool not found (skipping)"
orchestrate tools remove -n psvar_exemption_assessment_flow 2>/dev/null || echo "  - psvar_exemption_assessment_flow not found (skipping)"
orchestrate tools remove -n psvar_exemption_form_flow 2>/dev/null || echo "  - psvar_exemption_form_flow not found (skipping)"
orchestrate tools remove -n i__get_flow_status_intrinsic_tool__ 2>/dev/null || echo "  - i__get_flow_status_intrinsic_tool__ not found (skipping)"
orchestrate tools remove -n collect_applicant_details 2>/dev/null || echo "  - collect_applicant_details not found (skipping)"
orchestrate tools remove -n collect_declaration 2>/dev/null || echo "  - collect_declaration not found (skipping)"
orchestrate tools remove -n collect_stability_features 2>/dev/null || echo "  - collect_stability_features not found (skipping)"
orchestrate tools remove -n collect_schedule_requirements 2>/dev/null || echo "  - collect_schedule_requirements not found (skipping)"
orchestrate tools remove -n collect_payment_details 2>/dev/null || echo "  - collect_payment_details not found (skipping)"
orchestrate tools remove -n collect_vehicle_measurements 2>/dev/null || echo "  - collect_vehicle_measurements not found (skipping)"
orchestrate tools remove -n collect_vehicle_details 2>/dev/null || echo "  - collect_vehicle_details not found (skipping)"
orchestrate tools remove -n test_location_finder 2>/dev/null || echo "  - test_location_finder not found (skipping)"
orchestrate tools remove -n accessibility_assessment 2>/dev/null || echo "  - accessibility_assessment not found (skipping)"
orchestrate tools remove -n form_validation 2>/dev/null || echo "  - form_validation not found (skipping)"
orchestrate tools remove -n vehicle_lookup 2>/dev/null || echo "  - vehicle_lookup not found (skipping)"
orchestrate tools remove -n collect_alteration_details 2>/dev/null || echo "  - collect_alteration_details not found (skipping)"
orchestrate tools remove -n collect_capacity_data 2>/dev/null || echo "  - collect_capacity_data not found (skipping)"
orchestrate tools remove -n submit_complete_psva1_form 2>/dev/null || echo "  - submit_complete_psva1_form not found (skipping)"
orchestrate tools remove -n capacity_calculator 2>/dev/null || echo "  - capacity_calculator not found (skipping)"
orchestrate tools remove -n Agentic_workflow_6955oV 2>/dev/null || echo "  - Agentic_workflow_6955oV not found (skipping)"
orchestrate tools remove -n PSVAR_Exemption_Process_2018RR 2>/dev/null || echo "  - PSVAR_Exemption_Process_2018RR not found (skipping)"
echo "✓ Tools removed"
echo ""

# Clean generated files
echo "Cleaning generated files..."
rm -f generated/*.json 2>/dev/null || true
echo "✓ Generated files cleaned"
echo ""

echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
echo ""
echo "To verify cleanup, run:"
echo "  orchestrate agents list"
echo "  orchestrate tools list"
echo ""
echo "To re-import everything, run:"
echo "  ./import-all.sh"
echo ""

# Made with Bob