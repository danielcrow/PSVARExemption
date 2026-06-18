#!/usr/bin/env bash

# Import script for PSVAR Complete Assessment & Certificate Agent
# This script imports the certificate generation tool and the complete assessment agent

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "=========================================="
echo "PSVAR Complete Assessment Agent Import"
echo "=========================================="
echo ""

# Import the certificate generation tool
echo "Step 1: Importing certificate generation tool..."
orchestrate tools import -k python -f ${SCRIPT_DIR}/tools/create_certificate_from_assessment.py

if [ $? -eq 0 ]; then
    echo "✓ Certificate generation tool imported successfully"
else
    echo "✗ Failed to import certificate generation tool"
    exit 1
fi

echo ""

# Import the complete assessment agent
echo "Step 2: Importing complete assessment agent..."
orchestrate agents import -f ${SCRIPT_DIR}/agents/psvar_complete_assessment_agent.yaml

if [ $? -eq 0 ]; then
    echo "✓ Complete assessment agent imported successfully"
else
    echo "✗ Failed to import complete assessment agent"
    exit 1
fi

echo ""
echo "=========================================="
echo "Import Complete!"
echo "=========================================="
echo ""
echo "The following have been imported:"
echo "  - Tool: create_certificate_from_assessment"
echo "  - Agent: psvar_complete_assessment_agent"
echo ""
echo "To start using the agent:"
echo "  orchestrate chat start"
echo "  Then select: psvar_complete_assessment_agent"
echo ""
echo "The agent uses these existing tools:"
echo "  - evaluate_psvar_exemption (already imported)"
echo "  - send_assessment_outcome_email (already imported)"
echo ""

# Made with Bob
