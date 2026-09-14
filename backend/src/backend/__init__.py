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
    
class RiskCapacity(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    
class RiskTolerance(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    
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
    risk_tolerance = calculate_risk_tolerance(questionnaire)
    
    return {"questionnaire": questionnaire,
            "risk_capacity": risk_capacity,
            "risk_tolerance": risk_tolerance}
    
    
def calculate_risk_capacity(questionnaire: InvestorQuestionnaire) -> RiskCapacity:
    time_horizon = questionnaire.time_horizon_years
    liquidity_needs = questionnaire.liquidity_needs
    fund_reliance = questionnaire.fund_reliance
    
    risk_score = 0
    
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
            
    if risk_score < 6:
        risk_capacity = RiskCapacity.low
    elif risk_score == 6:
        risk_capacity = RiskCapacity.moderate
    else:
        risk_capacity = RiskCapacity.high
        
    if risk_capacity == RiskCapacity.high:
        if time_horizon <= 5 or liquidity_needs == LiquidityNeeds.high or fund_reliance == FundReliance.essential:
            risk_capacity = RiskCapacity.moderate
            
    return risk_capacity

def calculate_risk_tolerance(questionnaire: InvestorQuestionnaire) -> RiskTolerance:
    market_drop_response = questionnaire.market_drop_response
    investment_preference = questionnaire.investment_preference
    market_loss_comfort = questionnaire.market_loss_comfort
    
    risk_score = 0
    
    if market_drop_response == MarketDropResponse.sell_all:
        risk_score += 1
    elif market_drop_response == MarketDropResponse.sell_some:
        risk_score += 2
    elif market_drop_response == MarketDropResponse.hold:
        risk_score += 3
    elif market_drop_response == MarketDropResponse.invest_more:
        risk_score += 4
        
    if investment_preference == InvestmentPreference.lower_risk:
        risk_score += 1
    elif investment_preference == InvestmentPreference.balanced:
        risk_score += 2
    elif investment_preference == InvestmentPreference.higher_growth:
        risk_score += 3
        
    if market_loss_comfort == MarketLossComfort.very_uncomfortable:
        risk_score += 1
    elif market_loss_comfort == MarketLossComfort.somewhat_uncomfortable:
        risk_score += 2
    elif market_loss_comfort == MarketLossComfort.comfortable:
        risk_score += 3
    elif market_loss_comfort == MarketLossComfort.very_comfortable:
        risk_score += 4
            
    if risk_score < 5:
        risk_tolerance = RiskTolerance.low
    elif risk_score < 9:
        risk_tolerance = RiskTolerance.moderate
    else:
        risk_tolerance = RiskTolerance.high
        
    if risk_tolerance == RiskTolerance.high and investment_preference == InvestmentPreference.lower_risk:
        risk_tolerance = RiskTolerance.moderate
    
    return risk_tolerance
    