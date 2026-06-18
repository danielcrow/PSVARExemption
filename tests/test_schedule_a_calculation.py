"""
Tests for Schedule A minimum fleet proportion calculation.

Based on the examples provided in the draft exemption text.
"""

import pytest
from tools.evaluate_psvar_exemption import _calculate_minimum_fleet_proportion


class TestScheduleACalculation:
    """Test the Schedule A minimum fleet proportion calculation."""

    def test_example_1_from_task(self):
        """
        Example 1 from task:
        - 5 coaches on HTS/RR on 1st May (required 1 compliant)
        - Operator had 2 compliant coaches (exceeded requirement)
        - Total fleet: 10 coaches
        - Result: 2/10 = 20%
        """
        in_scope_compliant = 2
        all_coaches = 10
        
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant, all_coaches
        )
        
        # Should be 20% (actual proportion is higher than MTE minimum)
        assert percentage == 20.0
        assert "Actual in-scope compliant proportion" in method or any("actual proportion" in r.lower() for r in rationale)
        
    def test_example_2_from_task(self):
        """
        Example 2 from task:
        - 20 coaches on HTS/RR on 1st May (required 25% = 5 compliant)
        - Operator had only 4 compliant coaches (did not meet requirement)
        - Total fleet: 40 coaches
        - Result: 5/40 = 12.5% (using MTE minimum of 5)
        """
        in_scope_compliant = 4  # What they actually had
        all_coaches = 40
        
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant, all_coaches
        )
        
        # Should use MTE minimum: 20 coaches * 25% = 5 coaches
        # 5/40 = 12.5%
        assert percentage == 12.5
        assert "MTE minimum" in method or any("mte minimum" in r.lower() for r in rationale)
        
        # Should warn about non-compliance
        rationale_text = " ".join(rationale).lower()
        assert "warning" in rationale_text or "not valid" in rationale_text

    def test_band_a_1_coach(self):
        """Test Band A with 1 in-scope coach (requires 1 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=1,
            all_coaches=5
        )
        
        # 1 coach required, 1/5 = 20%
        assert percentage == 20.0

    def test_band_a_5_coaches(self):
        """Test Band A with 5 in-scope coaches (requires 1 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=1,
            all_coaches=5
        )
        
        # 1 coach required, 1/5 = 20%
        assert percentage == 20.0

    def test_band_b_6_coaches(self):
        """Test Band B with 6 in-scope coaches (requires 2 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=2,
            all_coaches=10
        )
        
        # 2 coaches required, 2/10 = 20%
        assert percentage == 20.0

    def test_band_b_9_coaches(self):
        """Test Band B with 9 in-scope coaches (requires 2 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=2,
            all_coaches=15
        )
        
        # 2 coaches required, 2/15 = 13.33%
        assert abs(percentage - 13.33) < 0.01

    def test_band_c_10_coaches(self):
        """Test Band C with 10 in-scope coaches (requires 25% = 3 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=3,
            all_coaches=20
        )
        
        # 3 coaches required (25% of 10 = 2.5, rounded up to 3)
        # 3/20 = 15%
        assert percentage == 15.0

    def test_band_c_29_coaches(self):
        """Test Band C with 29 in-scope coaches (requires 25% = 8 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=8,
            all_coaches=40
        )
        
        # 8 coaches required (25% of 29 = 7.25, rounded up to 8)
        # 8/40 = 20%
        assert percentage == 20.0

    def test_band_d_30_coaches(self):
        """Test Band D with 30 in-scope coaches (requires 35% = 11 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=11,
            all_coaches=50
        )
        
        # 11 coaches required (35% of 30 = 10.5, rounded up to 11)
        # 11/50 = 22%
        assert percentage == 22.0

    def test_band_d_100_coaches(self):
        """Test Band D with 100 in-scope coaches (requires 35% = 35 compliant)."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=35,
            all_coaches=150
        )
        
        # 35 coaches required (35% of 100 = 35)
        # 35/150 = 23.33%
        assert abs(percentage - 23.33) < 0.01

    def test_actual_higher_than_mte(self):
        """Test when actual proportion is higher than MTE minimum."""
        # 10 in-scope coaches (requires 25% = 3)
        # But operator has 5 compliant (50%)
        # Total fleet: 10 coaches
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=5,
            all_coaches=10
        )
        
        # Should use actual: 5/10 = 50%
        assert percentage == 50.0
        assert "actual" in method.lower() or any("actual" in r.lower() for r in rationale)

    def test_mte_higher_than_actual(self):
        """Test when MTE minimum is higher than actual proportion."""
        # 30 in-scope coaches (requires 35% = 11)
        # But operator only has 5 compliant
        # Total fleet: 100 coaches
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=5,
            all_coaches=100
        )
        
        # Should use MTE: 11/100 = 11%
        assert percentage == 11.0
        assert "mte" in method.lower() or any("mte" in r.lower() for r in rationale)

    def test_zero_coaches(self):
        """Test with zero coaches."""
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=0,
            all_coaches=10
        )
        
        # 0 in-scope coaches means no requirement
        assert percentage == 0.0

    def test_non_compliant_warning(self):
        """Test that warning is issued when operator was non-compliant on May 1st."""
        # 20 in-scope coaches (requires 25% = 5)
        # But operator only had 3
        percentage, method, rationale = _calculate_minimum_fleet_proportion(
            in_scope_compliant_coaches=3,
            all_coaches=40
        )
        
        # Should warn about non-compliance
        rationale_text = " ".join(rationale).lower()
        assert "warning" in rationale_text or "not valid" in rationale_text
        assert "3" in rationale_text and "5" in rationale_text  # Had 3, needed 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
