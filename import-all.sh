#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "=========================================="
echo "Importing PSVAR Intake Agent and Tools"
echo "=========================================="
echo ""

# Import Python tools required by psvar_intake_agent
echo "Importing Python tools..."
orchestrate tools import -k python -f ${SCRIPT_DIR}/tools/evaluate_psvar_exemption.py
orchestrate tools import -k python -f ${SCRIPT_DIR}/tools/send_assessment_outcome_email.py --app-id gmail_connection
echo "✓ Python tools imported"
echo ""

# Import Flow tools required by psvar_intake_agent
echo "Importing Flow tools..."
for flow in psvar_exemption_assessment_flow.py; do
  orchestrate tools import -k flow -f ${SCRIPT_DIR}/tools/${flow}
done
echo "✓ Flow tools imported"
echo ""

# Import only psvar_intake_agent
echo "Importing agent..."
orchestrate agents import -f ${SCRIPT_DIR}/agents/psvar_intake_agent.yaml
echo "✓ Agent imported"
echo ""

echo "=========================================="
echo "Import Complete!"
echo "=========================================="
echo ""
echo "Imported:"
echo "  - psvar_intake_agent (agent)"
echo "  - evaluate_psvar_exemption (tool)"
echo "  - send_assessment_outcome_email (tool)"
echo "  - psvar_exemption_assessment_flow (flow)"
echo ""
echo "To start chatting, run:"
echo "  orchestrate chat start"
echo ""

# Made with Bob
