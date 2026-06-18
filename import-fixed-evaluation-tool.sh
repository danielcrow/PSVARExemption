#!/usr/bin/env bash

echo "=========================================="
echo "PSVAR Evaluation Tool - Import Fixed Version"
echo "=========================================="
echo ""
echo "This script imports the corrected evaluate_psvar_exemption tool"
echo "that fixes the 'paying customers' logic error."
echo ""
echo "Step 1: Importing evaluation tool..."

orchestrate tools import -k python -f tools/evaluate_psvar_exemption.py

if [ $? -eq 0 ]; then
    echo "✓ Evaluation tool imported successfully"
    echo ""
    echo "=========================================="
    echo "Import Complete!"
    echo "=========================================="
    echo ""
    echo "The fix corrects the logic so that:"
    echo "  - HTS services WITH paying customers = OUT OF SCOPE"
    echo "  - HTS services WITHOUT paying customers = IN SCOPE for exemption"
    echo ""
    echo "You can now test the agent with free, closed-door HTS services."
else
    echo "✗ Failed to import evaluation tool"
    exit 1
fi

# Made with Bob
