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
    non_essential = "non-essential"

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
    risk_capacity = calculate_risk_capacity(questionnaire)
    
    return {"questionnaire": questionnaire,
            "risk_capacity": risk_capacity}
    
    
def calculate_risk_capacity(questionnaire: InvestorQuestionnaire) -> str:
    time_horizon = questionnaire.time_horizon_years
    liquidity_needs = questionnaire.liquidity_needs
    fund_reliance = questionnaire.fund_reliance
    
    risk_score = 0.0
    
    if time_horizon < 6:
        risk_score += 1
    elif time_horizon < 11:
        risk_score += 2
    else:
        risk_score += 3
    
    if liquidity_needs == LiquidityNeeds.high:
        risk_score += 1
    elif liquidity_needs == LiquidityNeeds.medium:
        risk_score += 2
    elif liquidity_needs == LiquidityNeeds.low:
        risk_score += 3
    
    if fund_reliance == FundReliance.essential:
        risk_score += 1
    elif fund_reliance == FundReliance.important:
        risk_score += 2
    elif fund_reliance == FundReliance.non_essential:
        risk_score += 3
        
    risk_score /= 3
            
    if risk_score < 1.67:
        risk_capacity = "low"
    elif risk_score < 2.34:
        risk_capacity = "moderate"
    else:
        risk_capacity = "high"
        
    if risk_capacity == "high":
        if time_horizon <= 5 or liquidity_needs == "high" or fund_reliance == "essential":
            risk_capacity = "moderate"
            
    return risk_capacity