import backend as InvestmentProfile
import pytest

@pytest.mark.parametrize(
    "time_horizon, liquidity, reliance, expected_risk",
    [
        (
            20,
            InvestmentProfile.LiquidityNeeds.low, 
            InvestmentProfile.FundReliance.non_essential,
            InvestmentProfile.RiskCapacity.high
        ),
        (
            3,
            InvestmentProfile.LiquidityNeeds.high, 
            InvestmentProfile.FundReliance.essential,
            InvestmentProfile.RiskCapacity.low
        ),
        (
            8,
            InvestmentProfile.LiquidityNeeds.medium, 
            InvestmentProfile.FundReliance.important,
            InvestmentProfile.RiskCapacity.moderate
        ),
        (
            4,
            InvestmentProfile.LiquidityNeeds.low,
            InvestmentProfile.FundReliance.non_essential,
            InvestmentProfile.RiskCapacity.moderate
        ),
        (
            50,
            InvestmentProfile.LiquidityNeeds.high,
            InvestmentProfile.FundReliance.non_essential,
            InvestmentProfile.RiskCapacity.moderate
        ),
        (
            40,
            InvestmentProfile.LiquidityNeeds.low,
            InvestmentProfile.FundReliance.essential,
            InvestmentProfile.RiskCapacity.moderate
        )
    ],
    ids=["high_risk", "low_risk", "moderate_risk", "short_horizon_caps_risk",
         "liquidity_guardrail", "fund_reliance_guardrail"]
)
def test_calculate_risk_capacity(time_horizon, liquidity, reliance, expected_risk):
    questionnaire = InvestmentProfile.InvestorQuestionnaire(
        goal=InvestmentProfile.InvestmentGoal.long_term_wealth,
        time_horizon_years=time_horizon,
        liquidity_needs=liquidity,
        fund_reliance=reliance,
        market_drop_response=InvestmentProfile.MarketDropResponse.hold,
        investment_preference=InvestmentProfile.InvestmentPreference.balanced,
        market_loss_comfort=InvestmentProfile.MarketLossComfort.comfortable,
        experience=InvestmentProfile.InvestingExperience.advanced
    )
    
    risk_capacity = InvestmentProfile.calculate_risk_capacity(questionnaire)
    
    assert risk_capacity == expected_risk
    
@pytest.mark.parametrize(
    "time_horizon, expected_risk",
    [
        (
            5,
            InvestmentProfile.RiskCapacity.moderate
        ),
        (
            6,
            InvestmentProfile.RiskCapacity.high
        ),
        (
            10,
            InvestmentProfile.RiskCapacity.high
        ),
        (
            11,
            InvestmentProfile.RiskCapacity.high
        )
    ],
    ids=["5 years", "6 years", "10 years", "11 years"]
)

def test_calculate_risk_capacity_boundaries(time_horizon, expected_risk):
    questionnaire = InvestmentProfile.InvestorQuestionnaire(
            goal=InvestmentProfile.InvestmentGoal.long_term_wealth,
            time_horizon_years=time_horizon,
            liquidity_needs=InvestmentProfile.LiquidityNeeds.low,
            fund_reliance=InvestmentProfile.FundReliance.non_essential,
            market_drop_response=InvestmentProfile.MarketDropResponse.hold,
            investment_preference=InvestmentProfile.InvestmentPreference.balanced,
            market_loss_comfort=InvestmentProfile.MarketLossComfort.comfortable,
            experience=InvestmentProfile.InvestingExperience.advanced
        )
        
    risk_capacity = InvestmentProfile.calculate_risk_capacity(questionnaire)
        
    assert risk_capacity == expected_risk 