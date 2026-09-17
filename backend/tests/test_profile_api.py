from fastapi.testclient import TestClient
import backend as InvestmentProfile
import pytest
from backend import app

client = TestClient(app)

def test_profile_call():
    
    questionnaire = InvestmentProfile.InvestorQuestionnaire(
        goal=InvestmentProfile.InvestmentGoal.retirement,
        time_horizon_years=1,
        liquidity_needs=InvestmentProfile.LiquidityNeeds.low,
        fund_reliance=InvestmentProfile.FundReliance.non_essential,
        market_drop_response=InvestmentProfile.MarketDropResponse.sell_all,
        investment_preference=InvestmentProfile.InvestmentPreference.lower_risk,
        market_loss_comfort=InvestmentProfile.MarketLossComfort.very_uncomfortable,
        experience=InvestmentProfile.InvestingExperience.beginner
    )
    
    response = client.post("/profile", json=questionnaire.model_dump(mode="json"))
    
    assert response.status_code == 200
    assert response.json() == {
        "questionnaire": {
            "goal": "retirement",
            "time_horizon_years": 1,
            "liquidity_needs": "low",
            "fund_reliance": "non-essential",
            "market_drop_response": "sell_all",
            "investment_preference": "lower_risk",
            "market_loss_comfort": "very_uncomfortable",
            "experience": "beginner"
        },
        "risk_capacity": "moderate",
        "risk_tolerance": "low",
        "risk_profile": "low",
        "profile_explanation": {
            "capacity_explanation": "Your financial circumstances indicate a moderate capacity for investment risk.",
            "tolerance_explanation": "Your responses indicate a low willingness to accept investment risk and market volatility.",
            "profile_explanation": "Your low risk tolerance keeps your overall risk profile at Low despite moderate risk capacity."
        }
    }
    
@pytest.mark.parametrize("field,value", [
    ("time_horizon_years", 0),
    ("time_horizon_years", 101),
])

def test_profile_rejects_invalid_questionnaire(field, value):
    questionnaire = {
        "goal": "retirement",
        "time_horizon_years": 20,
        "liquidity_needs": "low",
        "fund_reliance": "non-essential",
        "market_drop_response": "hold",
        "investment_preference": "balanced",
        "market_loss_comfort": "comfortable",
        "experience": "beginner"
    }

    questionnaire[field] = value
    response = client.post("/profile", json=questionnaire)

    assert response.status_code == 422
