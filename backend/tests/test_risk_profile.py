import backend as InvestmentProfile
import pytest

@pytest.mark.parametrize(
    "risk_capacity, risk_tolerance, expected_risk",
    [
        (
            InvestmentProfile.RiskCapacity.low,
            InvestmentProfile.RiskTolerance.low,
            InvestmentProfile.RiskProfile.very_low
        ),
        (
            InvestmentProfile.RiskCapacity.low,
            InvestmentProfile.RiskTolerance.moderate,
            InvestmentProfile.RiskProfile.low
        ),
        (
            InvestmentProfile.RiskCapacity.low,
            InvestmentProfile.RiskTolerance.high,
            InvestmentProfile.RiskProfile.moderate
        ),
        (
            InvestmentProfile.RiskCapacity.moderate,
            InvestmentProfile.RiskTolerance.low,
            InvestmentProfile.RiskProfile.low
        ),
        (
            InvestmentProfile.RiskCapacity.moderate,
            InvestmentProfile.RiskTolerance.moderate,
            InvestmentProfile.RiskProfile.moderate
        ),
        (
            InvestmentProfile.RiskCapacity.moderate,
            InvestmentProfile.RiskTolerance.high,
            InvestmentProfile.RiskProfile.high
        ),
        (
            InvestmentProfile.RiskCapacity.high,
            InvestmentProfile.RiskTolerance.low,
            InvestmentProfile.RiskProfile.moderate
        ),
        (
            InvestmentProfile.RiskCapacity.high,
            InvestmentProfile.RiskTolerance.moderate,
            InvestmentProfile.RiskProfile.high
        ),
        (
            InvestmentProfile.RiskCapacity.high,
            InvestmentProfile.RiskTolerance.high,
            InvestmentProfile.RiskProfile.very_high
        )
    ],
    ids=["low_low", "low_moderate", "low_high","moderate_low", "moderate_moderate",
         "moderate_high", "high_low", "high_moderate", "high_high"]
)
def test_calculate_risk_profile(risk_capacity, risk_tolerance, expected_risk):
    risk_profile = InvestmentProfile.calculate_risk_profile(risk_capacity, risk_tolerance)
    
    assert risk_profile == expected_risk