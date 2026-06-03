"""
PSVAR Exemption Assessment Flow - Programmatic Testing Script

This script allows you to test the PSVAR exemption assessment tool programmatically
without using the chat UI or flow invocation. It directly calls the evaluation tool
with test scenarios.

Usage:
    python3 main_flow.py
"""

import asyncio
from pathlib import Path
from datetime import date
from tools.psvar_exemption_assessment_flow import build_psvar_exemption_assessment_flow
from tools.evaluate_psvar_exemption import PSVARAssessmentInput, evaluate_psvar_exemption


async def test_fully_compliant_fleet():
    """Test scenario: Fully compliant fleet (no exemption needed)."""
    print("\n" + "=" * 80)
    print("TEST SCENARIO 1: Fully Compliant Fleet (No Exemption Needed)")
    print("=" * 80)
    
    test_input = PSVARAssessmentInput(
        company_name="Compliant Transport Ltd",
        operator_licence_number="OL123456",
        authorised_contact_name="John Smith",
        authorised_contact_telephone="01234567890",
        authorised_contact_email="john.smith@compliant-transport.com",
        authorised_contact_postal_address="123 Test Street, Test City",
        authorised_contact_postcode="TE1 2ST",
        service_types=["HTS"],
        hts_closed_door=True,
        hts_has_paying_customers=True,
        total_hts_rr_fleet_size=5,
        fully_compliant_vehicle_count=5,
        partially_compliant_vehicle_count=0,
        non_compliant_vehicle_count=0,
        vehicle_identification_numbers=[
            "1HGBH41JXMN109186",  # Valid VIN with check digit X
            "1HGBH41J7MN109193",  # Valid VIN with check digit 7
            "1HGBH41J4MN109202",  # Valid VIN with check digit 4
            "1HGBH41J1MN109219",  # Valid VIN with check digit 1
            "1HGBH41J8MN109226",  # Valid VIN with check digit 8
        ],
        exemption_certificate_exists=False,
        has_read_band_compliance_requirements=True,
        assessment_date=date.today().isoformat(),
    )
    
    return test_input


async def test_needs_exemption_certificate():
    """Test scenario: Fleet needs exemption certificate."""
    print("\n" + "=" * 80)
    print("TEST SCENARIO 2: Fleet Needs Exemption Certificate")
    print("=" * 80)
    
    test_input = PSVARAssessmentInput(
        company_name="Partial Compliance Transport Ltd",
        operator_licence_number="OL234567",
        authorised_contact_name="Jane Doe",
        authorised_contact_telephone="01234567891",
        authorised_contact_email="jane.doe@partial-transport.com",
        authorised_contact_postal_address="456 Test Avenue, Test Town",
        authorised_contact_postcode="TE2 3ST",
        service_types=["HTS"],
        hts_closed_door=True,
        hts_has_paying_customers=True,
        total_hts_rr_fleet_size=10,
        fully_compliant_vehicle_count=3,
        partially_compliant_vehicle_count=5,
        non_compliant_vehicle_count=2,
        vehicle_identification_numbers=[
            "1HGBH41JXMN109186",  # Fully compliant
            "1HGBH41J7MN109193",  # Fully compliant
            "1HGBH41J4MN109202",  # Fully compliant
            "1HGBH41J1MN109219",  # Partially compliant
            "1HGBH41J8MN109226",  # Partially compliant
            "1HGBH41J5MN109233",  # Partially compliant
            "1HGBH41J2MN109240",  # Partially compliant
            "1HGBH41J9MN109257",  # Partially compliant
            "1HGBH41J6MN109264",  # Non-compliant
            "1HGBH41J3MN109271",  # Non-compliant
        ],
        partially_compliant_vehicle_identification_numbers=[
            "1HGBH41J1MN109219",
            "1HGBH41J8MN109226",
            "1HGBH41J5MN109233",
            "1HGBH41J2MN109240",
            "1HGBH41J9MN109257",
        ],
        non_compliant_vehicle_identification_numbers=[
            "1HGBH41J6MN109264",
            "1HGBH41J3MN109271",
        ],
        exemption_certificate_exists=False,
        has_read_band_compliance_requirements=True,
        assessment_date=date.today().isoformat(),
    )
    
    return test_input


async def test_valid_exemption():
    """Test scenario: Valid exemption certificate with compliance."""
    print("\n" + "=" * 80)
    print("TEST SCENARIO 3: Valid Exemption Certificate")
    print("=" * 80)
    
    test_input = PSVARAssessmentInput(
        company_name="Exempt Transport Ltd",
        operator_licence_number="OL345678",
        authorised_contact_name="Bob Johnson",
        authorised_contact_telephone="01234567892",
        authorised_contact_email="bob.johnson@exempt-transport.com",
        authorised_contact_postal_address="789 Test Road, Test Village",
        authorised_contact_postcode="TE3 4ST",
        service_types=["HTS"],
        hts_closed_door=True,
        hts_has_paying_customers=True,
        total_hts_rr_fleet_size=8,
        fully_compliant_vehicle_count=2,
        partially_compliant_vehicle_count=4,
        non_compliant_vehicle_count=2,
        vehicle_identification_numbers=[
            "1HGBH41JXMN109186",  # Fully compliant
            "1HGBH41J7MN109193",  # Fully compliant
            "1HGBH41J4MN109202",  # Partially compliant
            "1HGBH41J1MN109219",  # Partially compliant
            "1HGBH41J8MN109226",  # Partially compliant
            "1HGBH41J5MN109233",  # Partially compliant
            "1HGBH41J2MN109240",  # Non-compliant
            "1HGBH41J9MN109257",  # Non-compliant
        ],
        partially_compliant_vehicle_identification_numbers=[
            "1HGBH41J4MN109202",
            "1HGBH41J1MN109219",
            "1HGBH41J8MN109226",
            "1HGBH41J5MN109233",
        ],
        non_compliant_vehicle_identification_numbers=[
            "1HGBH41J2MN109240",
            "1HGBH41J9MN109257",
        ],
        exemption_certificate_exists=True,
        exemption_start_date="2024-01-01",
        exemption_end_date="2026-07-31",
        exemption_certificate_reference="PSVAR-HTS-2024-001",
        exemption_copy_carried_onboard=True,
        alternative_accessible_transport_available=True,
        written_confirmation_retained=True,
        has_read_band_compliance_requirements=True,
        fleet_size_changed=False,
        assessment_date=date.today().isoformat(),
    )
    
    return test_input


async def test_out_of_scope():
    """Test scenario: Service out of scope (no paying customers)."""
    print("\n" + "=" * 80)
    print("TEST SCENARIO 4: Out of Scope (No Paying Customers)")
    print("=" * 80)
    
    test_input = PSVARAssessmentInput(
        company_name="Free Transport Ltd",
        operator_licence_number="OL456789",
        authorised_contact_name="Alice Brown",
        authorised_contact_telephone="01234567893",
        authorised_contact_email="alice.brown@free-transport.com",
        authorised_contact_postal_address="321 Test Lane, Test Borough",
        authorised_contact_postcode="TE4 5ST",
        service_types=["HTS"],
        hts_closed_door=True,
        hts_has_paying_customers=False,
        total_hts_rr_fleet_size=3,
        fully_compliant_vehicle_count=1,
        partially_compliant_vehicle_count=1,
        non_compliant_vehicle_count=1,
        vehicle_identification_numbers=[
            "1HGBH41JXMN109186",  # Fully compliant
            "1HGBH41J7MN109193",  # Partially compliant
            "1HGBH41J4MN109202",  # Non-compliant
        ],
        partially_compliant_vehicle_identification_numbers=[
            "1HGBH41J7MN109193",
        ],
        non_compliant_vehicle_identification_numbers=[
            "1HGBH41J4MN109202",
        ],
        exemption_certificate_exists=False,
        has_read_band_compliance_requirements=True,
        assessment_date=date.today().isoformat(),
    )
    
    return test_input


async def run_test_scenario(scenario_name: str, test_input: PSVARAssessmentInput):
    """Run a single test scenario and display results."""
    print(f"\nRunning {scenario_name}...")
    print("-" * 80)
    
    try:
        # Call the evaluation tool directly with the input object
        tool_response = evaluate_psvar_exemption(test_input)
        
        # ToolResponse wraps the actual PSVARAssessmentOutput - access via ['result']
        result = tool_response['result']
        
        print(f"\n✅ Assessment Complete")
        print(f"Decision: {result.decision}")
        print(f"Final Case Outcome: {result.final_case_outcome}")
        print(f"In Scope: {result.in_scope}")
        print(f"Exemption Needed: {result.exemption_needed}")
        print(f"Valid Certificate: {result.valid_exemption_certificate}")
        
        if result.compliance_band:
            print(f"Compliance Band: {result.compliance_band}")
            print(f"Milestone Compliant: {result.milestone_compliant}")
        
        print(f"\nRationale:")
        for item in result.rationale:
            print(f"  - {item}")
        
        print(f"\nNext Actions:")
        for item in result.next_actions:
            print(f"  - {item}")
        
        if result.missing_information:
            print(f"\nMissing Information:")
            for item in result.missing_information:
                print(f"  - {item}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test execution function."""
    print("\n" + "=" * 80)
    print("PSVAR EXEMPTION ASSESSMENT FLOW - PROGRAMMATIC TESTING")
    print("=" * 80)
    
    # Build and compile the flow
    print("\n📦 Building and compiling flow...")
    flow_def = await build_psvar_exemption_assessment_flow().compile_deploy()
    print("✅ Flow compiled successfully")
    
    # Save the flow specification
    generated_folder = Path(__file__).resolve().parent / "generated"
    generated_folder.mkdir(exist_ok=True)
    spec_path = generated_folder / "psvar_exemption_assessment_flow.json"
    flow_def.dump_spec(str(spec_path))
    print(f"✅ Flow specification saved to: {spec_path}")
    
    # Run test scenarios
    test_scenarios = [
        ("Scenario 1: Fully Compliant Fleet", await test_fully_compliant_fleet()),
        ("Scenario 2: Needs Exemption Certificate", await test_needs_exemption_certificate()),
        ("Scenario 3: Valid Exemption", await test_valid_exemption()),
        ("Scenario 4: Out of Scope", await test_out_of_scope()),
    ]
    
    results = []
    for scenario_name, test_input in test_scenarios:
        success = await run_test_scenario(scenario_name, test_input)
        results.append((scenario_name, success))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for scenario_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {scenario_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
