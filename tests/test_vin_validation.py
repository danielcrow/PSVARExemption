"""
Unit tests for VIN validation logic in the PSVAR exemption assessment tool.

These tests verify that Vehicle Identification Numbers (VINs) are properly
validated according to the standard VIN format and check digit algorithm.
"""

import pytest
from tools.evaluate_psvar_exemption import (
    _validate_vin,
    _normalize_vin,
    _calculate_vin_check_digit,
    _collect_vin_validation_issues,
)


class TestVINNormalization:
    """Tests for VIN normalization."""
    
    def test_normalize_uppercase(self):
        """Test that lowercase VINs are converted to uppercase."""
        assert _normalize_vin("1hgbh41jxmn109186") == "1HGBH41JXMN109186"
    
    def test_normalize_strips_whitespace(self):
        """Test that leading and trailing whitespace is removed."""
        assert _normalize_vin("  1HGBH41JXMN109186  ") == "1HGBH41JXMN109186"
    
    def test_normalize_mixed_case(self):
        """Test normalization of mixed case VINs."""
        assert _normalize_vin("1HgBh41JxMn109186") == "1HGBH41JXMN109186"
    
    def test_normalize_already_normalized(self):
        """Test that already normalized VINs remain unchanged."""
        assert _normalize_vin("1HGBH41JXMN109186") == "1HGBH41JXMN109186"


class TestVINCheckDigit:
    """Tests for VIN check digit calculation."""
    
    def test_calculate_check_digit_valid(self):
        """Test check digit calculation for a valid VIN."""
        # VIN without check digit: 1HGBH41J_MN109186
        # Expected check digit at position 9: X
        vin = "1HGBH41JXMN109186"
        check_digit = _calculate_vin_check_digit(vin)
        assert check_digit == "X"
    
    def test_calculate_check_digit_numeric(self):
        """Test check digit calculation resulting in a number."""
        # This VIN should have a numeric check digit
        vin = "2HGBH41JXMN109187"
        check_digit = _calculate_vin_check_digit(vin)
        assert check_digit in "0123456789X"
    
    def test_calculate_check_digit_consistency(self):
        """Test that check digit calculation is consistent."""
        vin = "1HGBH41JXMN109186"
        check_digit_1 = _calculate_vin_check_digit(vin)
        check_digit_2 = _calculate_vin_check_digit(vin)
        assert check_digit_1 == check_digit_2


class TestVINValidation:
    """Tests for VIN validation logic."""
    
    def test_valid_vin_passes(self):
        """Test that a valid VIN passes all validation checks."""
        errors = _validate_vin("1HGBH41JXMN109186")
        assert len(errors) == 0
    
    def test_valid_vin_lowercase_passes(self):
        """Test that a valid lowercase VIN passes after normalization."""
        errors = _validate_vin("1hgbh41jxmn109186")
        assert len(errors) == 0
    
    def test_invalid_length_too_short(self):
        """Test that VINs shorter than 17 characters fail validation."""
        errors = _validate_vin("1HGBH41JXMN10918")
        assert len(errors) == 1
        assert "must be exactly 17 characters long" in errors[0]
    
    def test_invalid_length_too_long(self):
        """Test that VINs longer than 17 characters fail validation."""
        errors = _validate_vin("1HGBH41JXMN1091866")
        assert len(errors) == 1
        assert "must be exactly 17 characters long" in errors[0]
    
    def test_invalid_character_i(self):
        """Test that VINs containing 'I' fail validation."""
        errors = _validate_vin("1HGBH41JXMN10918I")
        assert len(errors) > 0
        assert any("invalid characters" in error for error in errors)
    
    def test_invalid_character_o(self):
        """Test that VINs containing 'O' fail validation."""
        errors = _validate_vin("1HGBH41JXMN10918O")
        assert len(errors) > 0
        assert any("invalid characters" in error for error in errors)
    
    def test_invalid_character_q(self):
        """Test that VINs containing 'Q' fail validation."""
        errors = _validate_vin("1HGBH41JXMN10918Q")
        assert len(errors) > 0
        assert any("invalid characters" in error for error in errors)
    
    def test_invalid_special_characters(self):
        """Test that VINs with special characters fail validation."""
        errors = _validate_vin("1HGBH41JXMN10918-")
        assert len(errors) > 0
        assert any("invalid characters" in error for error in errors)
    
    def test_invalid_check_digit(self):
        """Test that VINs with incorrect check digits fail validation."""
        # Change the check digit from X to 0
        errors = _validate_vin("1HGBH41J0MN109186")
        assert len(errors) > 0
        assert any("invalid check digit" in error for error in errors)
    
    def test_multiple_validation_errors(self):
        """Test that multiple validation errors are reported."""
        # Too short AND contains invalid character
        errors = _validate_vin("1HGBH41JXMN1091I")
        # Should only report length error first
        assert len(errors) == 1
        assert "must be exactly 17 characters long" in errors[0]


class TestVINCollectionValidation:
    """Tests for validating collections of VINs."""
    
    def test_valid_vin_list(self):
        """Test that a list of valid VINs passes validation."""
        vins = [
            "1HGBH41JXMN109186",  # Valid VIN with check digit X
            "1HGBH41J7MN109193",  # Valid VIN with check digit 7
            "1HGBH41J4MN109202",  # Valid VIN with check digit 4
        ]
        rationale, missing_info = _collect_vin_validation_issues(vins, "test fleet")
        assert len(rationale) == 0
        assert len(missing_info) == 0
    
    def test_duplicate_vins_detected(self):
        """Test that duplicate VINs are detected and reported."""
        vins = [
            "1HGBH41JXMN109186",
            "1HGBH41JXMN109193",
            "1HGBH41JXMN109186",  # Duplicate
        ]
        rationale, missing_info = _collect_vin_validation_issues(vins, "test fleet")
        assert len(rationale) > 0
        assert any("Duplicate VINs" in item for item in rationale)
        assert len(missing_info) > 0
        assert any("unique valid VINs" in item for item in missing_info)
    
    def test_invalid_vin_in_list(self):
        """Test that invalid VINs in a list are detected."""
        vins = [
            "1HGBH41JXMN109186",
            "INVALID_VIN_HERE",  # Invalid
            "1HGBH41JXMN109193",
        ]
        rationale, missing_info = _collect_vin_validation_issues(vins, "test fleet")
        assert len(rationale) > 0
        assert any("INVALID_VIN_HERE" in item for item in rationale)
        assert len(missing_info) > 0
    
    def test_empty_vin_list(self):
        """Test that empty VIN lists pass validation."""
        vins = []
        rationale, missing_info = _collect_vin_validation_issues(vins, "test fleet")
        assert len(rationale) == 0
        assert len(missing_info) == 0
    
    def test_whitespace_only_vins_ignored(self):
        """Test that whitespace-only VINs are ignored."""
        vins = [
            "1HGBH41JXMN109186",
            "   ",  # Whitespace only
            "1HGBH41J7MN109193",
        ]
        rationale, missing_info = _collect_vin_validation_issues(vins, "test fleet")
        # Should only validate the two valid VINs
        assert len(rationale) == 0
        assert len(missing_info) == 0
    
    def test_multiple_issues_reported(self):
        """Test that multiple validation issues are all reported."""
        vins = [
            "1HGBH41JXMN109186",
            "1HGBH41JXMN109186",  # Duplicate
            "INVALID_VIN_HERE",    # Invalid
            "1HGBH41J0MN109186",   # Wrong check digit (should be X not 0)
        ]
        rationale, missing_info = _collect_vin_validation_issues(vins, "test fleet")
        # Should report duplicate + invalid VINs
        assert len(rationale) >= 2
        assert len(missing_info) >= 2


class TestVINEdgeCases:
    """Tests for edge cases in VIN validation."""
    
    def test_all_numeric_vin(self):
        """Test VIN with all numeric characters (except check digit position)."""
        # This is a valid format, though unusual
        errors = _validate_vin("12345678912345678")
        # May fail check digit validation, but should not fail character validation
        assert not any("invalid characters" in error for error in errors)
    
    def test_all_alpha_vin(self):
        """Test VIN with maximum alphabetic characters."""
        errors = _validate_vin("ABCDEFGHJKLMNPRST")
        # Should not fail character validation (no I, O, Q)
        assert not any("invalid characters" in error for error in errors)
    
    def test_vin_with_x_check_digit(self):
        """Test that VINs with 'X' as check digit are valid."""
        # X is a valid check digit (represents 10)
        errors = _validate_vin("1HGBH41JXMN109186")
        assert len(errors) == 0
    
    def test_case_insensitive_validation(self):
        """Test that validation is case-insensitive."""
        errors_upper = _validate_vin("1HGBH41JXMN109186")
        errors_lower = _validate_vin("1hgbh41jxmn109186")
        errors_mixed = _validate_vin("1HgBh41JxMn109186")
        
        # All should have the same validation result
        assert errors_upper == errors_lower == errors_mixed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
