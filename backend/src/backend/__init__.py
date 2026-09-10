from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class InvestmentGoal(str, Enum):
    retirement = "retirement"
    home = "home"
    long_term_wealth = "long_term_wealth"
    other = "other"

class MarketDropResponse(str, Enum):
    sell_all = "sell_all"
    sell_some = "sell_some"
    hold = "hold"
    invest_more = "invest_more"
    
class InvestingExperience(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    
class LiquidityNeeds(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    
class FundReliance(str, Enum):
    essential = "essential"
    important = "important"
    non_essential = "non_essential"

class InvestmentPreference(str, Enum):
    lower_risk = "lower_risk"
    balanced = "balanced"
    higher_growth = "higher_growth"

class MarketLossComfort(str, Enum):
    very_uncomfortable = "very_uncomfortable"
    somewhat_uncomfortable = "somewhat_uncomfortable"
    comfortable = "comfortable"
    very_comfortable = "very_comfortable"
    
class InvestorQuestionnaire(BaseModel):
    goal: InvestmentGoal
    time_horizon_years: int = Field(gt=0, le=100)
    liquidity_needs: LiquidityNeeds
    fund_reliance: FundReliance
    market_drop_response: MarketDropResponse
    investment_preference: InvestmentPreference
    market_loss_comfort: MarketLossComfort
    experience: InvestingExperience

@app.get("/")
def root():
    return {"message": "InvestLab API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/profile")
def create_profile(questionnaire: InvestorQuestionnaire):
    risk_capacity = 0.0
    
    return {"questionnaire": questionnaire,
            "risk_capacity": risk_capacity}
    