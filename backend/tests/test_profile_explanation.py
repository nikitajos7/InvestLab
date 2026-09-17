import pytest
import backend as InvestmentProfile

@pytest.mark.parametrize("risk_capacity,risk_tolerance", [
    (InvestmentProfile.RiskCapacity.low, InvestmentProfile.RiskTolerance.low),
    (InvestmentProfile.RiskCapacity.low, InvestmentProfile.RiskTolerance.moderate),
    (InvestmentProfile.RiskCapacity.low, InvestmentProfile.RiskTolerance.high),
    (InvestmentProfile.RiskCapacity.moderate, InvestmentProfile.RiskTolerance.low),
    (InvestmentProfile.RiskCapacity.moderate, InvestmentProfile.RiskTolerance.moderate),
    (InvestmentProfile.RiskCapacity.moderate, InvestmentProfile.RiskTolerance.high),
    (InvestmentProfile.RiskCapacity.high, InvestmentProfile.RiskTolerance.low),
    (InvestmentProfile.RiskCapacity.high, InvestmentProfile.RiskTolerance.moderate),
    (InvestmentProfile.RiskCapacity.high, InvestmentProfile.RiskTolerance.high),
])
def test_generate_profile_explanation(risk_capacity, risk_tolerance):
    result = InvestmentProfile.generate_profile_explanation(risk_capacity, risk_tolerance)

    assert isinstance(result, InvestmentProfile.ProfileExplanation)
    assert result.capacity_explanation == InvestmentProfile.CAPACITY_EXPLANATIONS[risk_capacity]
    assert result.tolerance_explanation == InvestmentProfile.TOLERANCE_EXPLANATIONS[risk_tolerance]
    assert result.profile_explanation == InvestmentProfile.PROFILE_EXPLANATIONS[(risk_capacity, risk_tolerance)]