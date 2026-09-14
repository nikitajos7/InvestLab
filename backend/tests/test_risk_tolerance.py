import backend as InvestmentProfile
import pytest

@pytest.mark.parametrize(
    "market_drop_response, investment_preference, market_loss_comfort, expected_risk",
    [
        (
            InvestmentProfile.MarketDropResponse.sell_all,
            InvestmentProfile.InvestmentPreference.lower_risk, 
            InvestmentProfile.MarketLossComfort.very_uncomfortable,
            InvestmentProfile.RiskTolerance.low
        ),
        (
            InvestmentProfile.MarketDropResponse.sell_some,
            InvestmentProfile.InvestmentPreference.balanced, 
            InvestmentProfile.MarketLossComfort.somewhat_uncomfortable,
            InvestmentProfile.RiskTolerance.moderate
        ),
        (
            InvestmentProfile.MarketDropResponse.hold,
            InvestmentProfile.InvestmentPreference.higher_growth, 
            InvestmentProfile.MarketLossComfort.very_comfortable,
            InvestmentProfile.RiskTolerance.high
        ),
        (
            InvestmentProfile.MarketDropResponse.invest_more,
            InvestmentProfile.InvestmentPreference.higher_growth, 
            InvestmentProfile.MarketLossComfort.very_comfortable,
            InvestmentProfile.RiskTolerance.high
        ),
        (
            InvestmentProfile.MarketDropResponse.invest_more,
            InvestmentProfile.InvestmentPreference.lower_risk, 
            InvestmentProfile.MarketLossComfort.very_comfortable,
            InvestmentProfile.RiskTolerance.moderate
        )
    ],
    ids=["low_risk", "moderate_risk", "medium_high_risk","high_high_risk", "investment_preference_guardrail"]
)
def test_calculate_risk_tolerance(market_drop_response, investment_preference, market_loss_comfort, expected_risk):
    questionnaire = InvestmentProfile.InvestorQuestionnaire(
        goal=InvestmentProfile.InvestmentGoal.long_term_wealth,
        time_horizon_years=20,
        liquidity_needs=InvestmentProfile.LiquidityNeeds.high,
        fund_reliance=InvestmentProfile.FundReliance.essential,
        market_drop_response=market_drop_response,
        investment_preference=investment_preference,
        market_loss_comfort=market_loss_comfort,
        experience=InvestmentProfile.InvestingExperience.advanced
    )
    
    risk_tolerance = InvestmentProfile.calculate_risk_tolerance(questionnaire)
    
    assert risk_tolerance == expected_risk
    
@pytest.mark.parametrize(
    "market_drop_response, investment_preference, market_loss_comfort, expected_risk",
    [
        (
            InvestmentProfile.MarketDropResponse.sell_all,
            InvestmentProfile.InvestmentPreference.balanced, 
            InvestmentProfile.MarketLossComfort.very_uncomfortable,
            InvestmentProfile.RiskTolerance.low
        ),
        (
            InvestmentProfile.MarketDropResponse.sell_some,
            InvestmentProfile.InvestmentPreference.balanced, 
            InvestmentProfile.MarketLossComfort.very_uncomfortable,
            InvestmentProfile.RiskTolerance.moderate
        ),
        (
            InvestmentProfile.MarketDropResponse.hold,
            InvestmentProfile.InvestmentPreference.higher_growth, 
            InvestmentProfile.MarketLossComfort.somewhat_uncomfortable,
            InvestmentProfile.RiskTolerance.moderate
        ),
        (
            InvestmentProfile.MarketDropResponse.invest_more,
            InvestmentProfile.InvestmentPreference.balanced, 
            InvestmentProfile.MarketLossComfort.comfortable,
            InvestmentProfile.RiskTolerance.high
        )
    ],
    ids=["4 boundary", "5 boundary", "8 boundary", "9 boundary"]
)
def test_calculate_risk_tolerance_boundaries(market_drop_response, investment_preference, market_loss_comfort, expected_risk):
    questionnaire = InvestmentProfile.InvestorQuestionnaire(
        goal=InvestmentProfile.InvestmentGoal.long_term_wealth,
        time_horizon_years=20,
        liquidity_needs=InvestmentProfile.LiquidityNeeds.high,
        fund_reliance=InvestmentProfile.FundReliance.essential,
        market_drop_response=market_drop_response,
        investment_preference=investment_preference,
        market_loss_comfort=market_loss_comfort,
        experience=InvestmentProfile.InvestingExperience.advanced
    )
    
    risk_tolerance = InvestmentProfile.calculate_risk_tolerance(questionnaire)
    
    assert risk_tolerance == expected_risk