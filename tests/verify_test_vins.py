"""
Helper script to verify that all VINs used in tests have valid check digits.
Run this to ensure test VINs are correct before running the full test suite.
"""

from tools.evaluate_psvar_exemption import _validate_vin, _normalize_vin


def verify_vin(vin: str, description: str = ""):
    """Verify a single VIN and print the result."""
    normalized = _normalize_vin(vin)
    errors = _validate_vin(normalized)
    
    if errors:
        print(f"❌ INVALID: {vin} {description}")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print(f"✅ VALID: {vin} {description}")
        return True


def main():
    """Verify all VINs used in tests."""
    print("=" * 80)
    print("VIN Validation Check for Test Suite")
    print("=" * 80)
    
    test_vins = [
        # From test_vin_validation.py
        ("1HGBH41JXMN109186", "Primary test VIN"),
        ("1HGBH41JXMN109193", "Test VIN 2"),
        ("1HGBH41JXMN109202", "Test VIN 3"),
        
        # From main_flow.py - Scenario 1
        ("1HGBH41JXMN109186", "Scenario 1 - Vehicle 1"),
        ("1HGBH41JXMN109193", "Scenario 1 - Vehicle 2"),
        ("1HGBH41JXMN109202", "Scenario 1 - Vehicle 3"),
        ("1HGBH41JXMN109219", "Scenario 1 - Vehicle 4"),
        ("1HGBH41JXMN109226", "Scenario 1 - Vehicle 5"),
        
        # From main_flow.py - Scenario 2
        ("1HGBH41JXMN109233", "Scenario 2 - Vehicle 6"),
        ("1HGBH41JXMN109240", "Scenario 2 - Vehicle 7"),
        ("1HGBH41JXMN109257", "Scenario 2 - Vehicle 8"),
        ("1HGBH41JXMN109264", "Scenario 2 - Vehicle 9"),
        ("1HGBH41JXMN109271", "Scenario 2 - Vehicle 10"),
    ]
    
    all_valid = True
    for vin, description in test_vins:
        if not verify_vin(vin, f"({description})"):
            all_valid = False
    
    print("=" * 80)
    if all_valid:
        print("✅ All test VINs are valid!")
    else:
        print("❌ Some test VINs are invalid - please fix them")
    print("=" * 80)
    
    return 0 if all_valid else 1


if __name__ == "__main__":
    exit(main())

# Made with Bob
