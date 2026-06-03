"""
Unit tests for compliance band evaluation logic in the PSVAR exemption assessment tool.

These tests verify that fleet compliance bands are correctly determined and that
milestone requirements are properly evaluated based on fleet size and assessment date.
"""

import pytest
from datetime import date
from tools.evaluate_psvar_exemption import (
    _determine_band,
    _required_counts_for_date,
    _evaluate_milestone,
)


class TestBandDetermination:
    """Tests for determining compliance bands based on fleet size."""
    
    def test_band_a_minimum(self):
        """Test that fleet size 1 is assigned to Band A."""
        assert _determine_band(1) == "A"
    
    def test_band_a_maximum(self):
        """Test that fleet size 5 is assigned to Band A."""
        assert _determine_band(5) == "A"
    
    def test_band_a_middle(self):
        """Test that fleet size 3 is assigned to Band A."""
        assert _determine_band(3) == "A"
    
    def test_band_b_minimum(self):
        """Test that fleet size 6 is assigned to Band B."""
        assert _determine_band(6) == "B"
    
    def test_band_b_maximum(self):
        """Test that fleet size 9 is assigned to Band B."""
        assert _determine_band(9) == "B"
    
    def test_band_b_middle(self):
        """Test that fleet size 7 is assigned to Band B."""
        assert _determine_band(7) == "B"
    
    def test_band_c_minimum(self):
        """Test that fleet size 10 is assigned to Band C."""
        assert _determine_band(10) == "C"
    
    def test_band_c_maximum(self):
        """Test that fleet size 29 is assigned to Band C."""
        assert _determine_band(29) == "C"
    
    def test_band_c_middle(self):
        """Test that fleet size 20 is assigned to Band C."""
        assert _determine_band(20) == "C"
    
    def test_band_d_minimum(self):
        """Test that fleet size 30 is assigned to Band D."""
        assert _determine_band(30) == "D"
    
    def test_band_d_large(self):
        """Test that large fleet sizes are assigned to Band D."""
        assert _determine_band(100) == "D"
        assert _determine_band(500) == "D"
    
    def test_zero_fleet_size(self):
        """Test that zero fleet size returns None."""
        assert _determine_band(0) is None
    
    def test_negative_fleet_size(self):
        """Test that negative fleet size returns None."""
        assert _determine_band(-1) is None


class TestRequiredCountsForDate:
    """Tests for determining required vehicle counts based on band and date."""
    
    def test_band_a_before_2023_08_01(self):
        """Test Band A requirements before the exemption regime starts."""
        requirements = _required_counts_for_date("A", 5, date(2023, 7, 31))
        assert requirements["minimum_fully_compliant"] == 0
        assert requirements["minimum_partially_compliant"] == 0
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_a_first_milestone(self):
        """Test Band A requirements during first milestone (Aug 2023 - Jul 2024)."""
        requirements = _required_counts_for_date("A", 5, date(2024, 1, 1))
        assert requirements["minimum_fully_compliant"] == 0
        assert requirements["minimum_partially_compliant"] == 2  # 25% of 5 = 1.25, ceil = 2
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_a_second_milestone(self):
        """Test Band A requirements during second milestone (Aug 2024 - Jul 2025)."""
        requirements = _required_counts_for_date("A", 5, date(2024, 12, 1))
        assert requirements["minimum_fully_compliant"] == 0
        assert requirements["minimum_partially_compliant"] == 3  # 50% of 5 = 2.5, ceil = 3
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_a_final_milestone(self):
        """Test Band A requirements during final milestone (Aug 2025 onwards)."""
        requirements = _required_counts_for_date("A", 5, date(2025, 8, 1))
        assert requirements["minimum_fully_compliant"] == 1
        assert requirements["minimum_partially_compliant"] == 0
        assert requirements["remaining_must_be_partially_compliant"] is True
    
    def test_band_b_first_milestone(self):
        """Test Band B requirements during first milestone."""
        requirements = _required_counts_for_date("B", 8, date(2024, 1, 1))
        assert requirements["minimum_fully_compliant"] == 0
        assert requirements["minimum_partially_compliant"] == 2  # 25% of 8 = 2
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_b_second_milestone(self):
        """Test Band B requirements during second milestone."""
        requirements = _required_counts_for_date("B", 8, date(2024, 12, 1))
        assert requirements["minimum_fully_compliant"] == 1
        assert requirements["minimum_partially_compliant"] == 4  # 50% of 8 = 4
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_b_final_milestone(self):
        """Test Band B requirements during final milestone."""
        requirements = _required_counts_for_date("B", 8, date(2025, 8, 1))
        assert requirements["minimum_fully_compliant"] == 2
        assert requirements["minimum_partially_compliant"] == 0
        assert requirements["remaining_must_be_partially_compliant"] is True
    
    def test_band_c_first_milestone(self):
        """Test Band C requirements during first milestone."""
        requirements = _required_counts_for_date("C", 20, date(2024, 1, 1))
        assert requirements["minimum_fully_compliant"] == 0
        assert requirements["minimum_partially_compliant"] == 5  # 25% of 20 = 5
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_c_second_milestone(self):
        """Test Band C requirements during second milestone."""
        requirements = _required_counts_for_date("C", 20, date(2024, 12, 1))
        assert requirements["minimum_fully_compliant"] == 3  # 15% of 20 = 3
        assert requirements["minimum_partially_compliant"] == 10  # 50% of 20 = 10
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_c_final_milestone(self):
        """Test Band C requirements during final milestone."""
        requirements = _required_counts_for_date("C", 20, date(2025, 8, 1))
        assert requirements["minimum_fully_compliant"] == 5  # 25% of 20 = 5
        assert requirements["minimum_partially_compliant"] == 0
        assert requirements["remaining_must_be_partially_compliant"] is True
    
    def test_band_d_first_milestone(self):
        """Test Band D requirements during first milestone."""
        requirements = _required_counts_for_date("D", 100, date(2024, 1, 1))
        assert requirements["minimum_fully_compliant"] == 15  # 15% of 100 = 15
        assert requirements["minimum_partially_compliant"] == 25  # 25% of 100 = 25
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_d_second_milestone(self):
        """Test Band D requirements during second milestone."""
        requirements = _required_counts_for_date("D", 100, date(2024, 12, 1))
        assert requirements["minimum_fully_compliant"] == 25  # 25% of 100 = 25
        assert requirements["minimum_partially_compliant"] == 50  # 50% of 100 = 50
        assert requirements["remaining_must_be_partially_compliant"] is False
    
    def test_band_d_final_milestone(self):
        """Test Band D requirements during final milestone."""
        requirements = _required_counts_for_date("D", 100, date(2025, 8, 1))
        assert requirements["minimum_fully_compliant"] == 35  # 35% of 100 = 35
        assert requirements["minimum_partially_compliant"] == 0
        assert requirements["remaining_must_be_partially_compliant"] is True


class TestMilestoneEvaluation:
    """Tests for evaluating whether a fleet meets milestone requirements."""
    
    def test_band_a_compliant_first_milestone(self):
        """Test Band A fleet that meets first milestone requirements."""
        compliant, reasons = _evaluate_milestone(
            band="A",
            fleet_size=5,
            fully_compliant=0,
            partially_compliant=2,
            non_compliant=3,
            as_of=date(2024, 1, 1)
        )
        assert compliant is True
        assert len(reasons) == 0
    
    def test_band_a_non_compliant_first_milestone(self):
        """Test Band A fleet that fails first milestone requirements."""
        compliant, reasons = _evaluate_milestone(
            band="A",
            fleet_size=5,
            fully_compliant=0,
            partially_compliant=1,  # Need 2
            non_compliant=4,
            as_of=date(2024, 1, 1)
        )
        assert compliant is False
        assert len(reasons) > 0
        assert any("partially compliant" in reason for reason in reasons)
    
    def test_band_a_compliant_final_milestone(self):
        """Test Band A fleet that meets final milestone requirements."""
        compliant, reasons = _evaluate_milestone(
            band="A",
            fleet_size=5,
            fully_compliant=1,
            partially_compliant=4,
            non_compliant=0,
            as_of=date(2025, 8, 1)
        )
        assert compliant is True
        assert len(reasons) == 0
    
    def test_band_a_non_compliant_final_milestone_no_fully_compliant(self):
        """Test Band A fleet that fails final milestone (no fully compliant)."""
        compliant, reasons = _evaluate_milestone(
            band="A",
            fleet_size=5,
            fully_compliant=0,  # Need 1
            partially_compliant=5,
            non_compliant=0,
            as_of=date(2025, 8, 1)
        )
        assert compliant is False
        assert len(reasons) > 0
        assert any("fully compliant" in reason for reason in reasons)
    
    def test_band_a_non_compliant_final_milestone_has_non_compliant(self):
        """Test Band A fleet that fails final milestone (has non-compliant vehicles)."""
        compliant, reasons = _evaluate_milestone(
            band="A",
            fleet_size=5,
            fully_compliant=1,
            partially_compliant=3,
            non_compliant=1,  # Not allowed at this stage
            as_of=date(2025, 8, 1)
        )
        assert compliant is False
        assert len(reasons) > 0
        assert any("remaining vehicles" in reason for reason in reasons)
    
    def test_band_b_compliant_second_milestone(self):
        """Test Band B fleet that meets second milestone requirements."""
        compliant, reasons = _evaluate_milestone(
            band="B",
            fleet_size=8,
            fully_compliant=1,
            partially_compliant=4,
            non_compliant=3,
            as_of=date(2024, 12, 1)
        )
        assert compliant is True
        assert len(reasons) == 0
    
    def test_band_c_compliant_second_milestone(self):
        """Test Band C fleet that meets second milestone requirements."""
        compliant, reasons = _evaluate_milestone(
            band="C",
            fleet_size=20,
            fully_compliant=3,
            partially_compliant=10,
            non_compliant=7,
            as_of=date(2024, 12, 1)
        )
        assert compliant is True
        assert len(reasons) == 0
    
    def test_band_d_non_compliant_first_milestone(self):
        """Test Band D fleet that fails first milestone requirements."""
        compliant, reasons = _evaluate_milestone(
            band="D",
            fleet_size=100,
            fully_compliant=10,  # Need 15
            partially_compliant=20,  # Need 25
            non_compliant=70,
            as_of=date(2024, 1, 1)
        )
        assert compliant is False
        assert len(reasons) >= 2  # Should fail both fully and partially compliant requirements
    
    def test_before_exemption_regime_always_compliant(self):
        """Test that fleets before Aug 2023 are always considered compliant."""
        compliant, reasons = _evaluate_milestone(
            band="D",
            fleet_size=100,
            fully_compliant=0,
            partially_compliant=0,
            non_compliant=100,
            as_of=date(2023, 7, 31)
        )
        assert compliant is True
        assert len(reasons) == 0


class TestEdgeCases:
    """Tests for edge cases in band evaluation."""
    
    def test_exact_milestone_date_boundaries(self):
        """Test behavior on exact milestone date boundaries."""
        # Test on Aug 1, 2024 (start of second milestone)
        requirements = _required_counts_for_date("A", 5, date(2024, 8, 1))
        assert requirements["minimum_partially_compliant"] == 3  # Second milestone
        
        # Test on Jul 31, 2024 (end of first milestone)
        requirements = _required_counts_for_date("A", 5, date(2024, 7, 31))
        assert requirements["minimum_partially_compliant"] == 2  # First milestone
    
    def test_ceiling_calculation_for_percentages(self):
        """Test that percentage calculations use ceiling (round up)."""
        # 25% of 7 = 1.75, should ceil to 2
        requirements = _required_counts_for_date("B", 7, date(2024, 1, 1))
        assert requirements["minimum_partially_compliant"] == 2
        
        # 15% of 13 = 1.95, should ceil to 2
        requirements = _required_counts_for_date("C", 13, date(2024, 12, 1))
        assert requirements["minimum_fully_compliant"] == 2
    
    def test_single_vehicle_fleet(self):
        """Test Band A with single vehicle."""
        requirements = _required_counts_for_date("A", 1, date(2025, 8, 1))
        assert requirements["minimum_fully_compliant"] == 1
        assert requirements["remaining_must_be_partially_compliant"] is True
    
    def test_large_fleet_band_d(self):
        """Test Band D with very large fleet."""
        requirements = _required_counts_for_date("D", 500, date(2025, 8, 1))
        assert requirements["minimum_fully_compliant"] == 175  # 35% of 500
        assert requirements["remaining_must_be_partially_compliant"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
