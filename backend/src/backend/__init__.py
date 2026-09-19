from enum import Enum
import math

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

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
    
class RiskProfile(str, Enum):
    very_low = "very_low"
    low = "low"
    moderate = "moderate"
    high = "high"
    very_high = "very_high"
    
CAPACITY_EXPLANATIONS = {
    RiskCapacity.low: "Your financial circumstances indicate a low capacity for investment risk.",
    RiskCapacity.moderate: "Your financial circumstances indicate a moderate capacity for investment risk.",
    RiskCapacity.high: "Your financial circumstances indicate a high capacity for investment risk.",
}

TOLERANCE_EXPLANATIONS = {
    RiskTolerance.low: "Your responses indicate a low willingness to accept investment risk and market volatility.",
    RiskTolerance.moderate: "Your responses indicate a moderate willingness to accept investment risk and market volatility.",
    RiskTolerance.high: "Your responses indicate a high willingness to accept investment risk and market volatility.",
}

PROFILE_EXPLANATIONS = {
    (RiskCapacity.low, RiskTolerance.low): "Your low risk capacity and low risk tolerance result in a Very Low overall risk profile.",
    (RiskCapacity.low, RiskTolerance.moderate): "Your low risk capacity keeps your overall risk profile at Low despite moderate risk tolerance.",
    (RiskCapacity.low, RiskTolerance.high): "Your high risk tolerance raises your overall profile, but low risk capacity limits it to Moderate.",
    (RiskCapacity.moderate, RiskTolerance.low): "Your low risk tolerance keeps your overall risk profile at Low despite moderate risk capacity.",
    (RiskCapacity.moderate, RiskTolerance.moderate): "Your moderate risk capacity and tolerance result in a Moderate overall risk profile.",
    (RiskCapacity.moderate, RiskTolerance.high): "Your high risk tolerance combined with moderate risk capacity results in a High overall risk profile.",
    (RiskCapacity.high, RiskTolerance.low): "Although your risk capacity is high, low risk tolerance limits your overall risk profile to Moderate.",
    (RiskCapacity.high, RiskTolerance.moderate): "Your high risk capacity supports greater risk, while moderate risk tolerance limits your overall profile to High.",
    (RiskCapacity.high, RiskTolerance.high): "Your high risk capacity and high risk tolerance result in a Very High overall risk profile.",
}

class ProfileExplanation(BaseModel):
    capacity_explanation: str
    tolerance_explanation: str
    profile_explanation: str
    
class InvestorQuestionnaire(BaseModel):
    goal: InvestmentGoal
    time_horizon_years: int = Field(gt=0, le=100)
    liquidity_needs: LiquidityNeeds
    fund_reliance: FundReliance
    market_drop_response: MarketDropResponse
    investment_preference: InvestmentPreference
    market_loss_comfort: MarketLossComfort
    experience: InvestingExperience

class InvestorProfile(BaseModel):
    questionnaire: InvestorQuestionnaire
    risk_capacity: RiskCapacity
    risk_tolerance: RiskTolerance
    risk_profile: RiskProfile
    profile_explanation: ProfileExplanation
    
class AssetAllocation(BaseModel):
    stocks: float = Field(ge=0, le=1)
    bonds: float = Field(ge=0, le=1)
    cash: float = Field(ge=0, le=1)
    
    @model_validator(mode="after")
    def validate_allocation(self):
        total = self.stocks + self.bonds + self.cash
        if not math.isclose(total, 1.0):
            raise ValueError("The sum of stocks, bonds, and cash must be approximately 1.")
        return self
    
ASSET_ALLOCATIONS = {
    RiskProfile.very_low: {"stocks": 0.2, "bonds": 0.5, "cash": 0.3},
    RiskProfile.low: {"stocks": 0.4, "bonds": 0.5, "cash": 0.1},
    RiskProfile.moderate: {"stocks": 0.6, "bonds": 0.35, "cash": 0.05},
    RiskProfile.high: {"stocks": 0.8, "bonds": 0.15, "cash": 0.05},
    RiskProfile.very_high: {"stocks": 0.95, "bonds": 0.0, "cash": 0.05},
}

US_STOCK_WEIGHT = 0.60
INTERNATIONAL_STOCK_WEIGHT = 0.40

US_BOND_WEIGHT = 0.70
INTERNATIONAL_BOND_WEIGHT = 0.30
    
class PortfolioAllocation(BaseModel):
    us_stocks: float = Field(ge=0, le=1)
    international_stocks: float = Field(ge=0, le=1)
    us_bonds: float = Field(ge=0, le=1)
    international_bonds: float = Field(ge=0, le=1)
    cash: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def validate_allocation(self):
        total = self.us_stocks + self.international_stocks + self.us_bonds + self.international_bonds + self.cash
        if not math.isclose(total, 1.0):
            raise ValueError("The sum of all asset classes must be approximately 1.")
        return self

@app.get("/")
def root():
    return {"message": "InvestLab API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/profile", response_model=InvestorProfile)
def create_profile(questionnaire: InvestorQuestionnaire):
    risk_capacity = calculate_risk_capacity(questionnaire)
    risk_tolerance = calculate_risk_tolerance(questionnaire)
    
    risk_profile = calculate_risk_profile(risk_capacity, risk_tolerance)
    
    profile_explanation = generate_profile_explanation(risk_capacity, risk_tolerance)
    
    investor_profile = InvestorProfile(
        questionnaire=questionnaire,
        risk_capacity=risk_capacity,
        risk_tolerance=risk_tolerance,
        risk_profile=risk_profile,
        profile_explanation=profile_explanation
    )

    return investor_profile
    
    
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

def calculate_risk_profile(risk_capacity: RiskCapacity, risk_tolerance: RiskTolerance) -> RiskProfile:
    risk_capacity_score = 0
    risk_tolerance_score = 0
    
    if risk_capacity == RiskCapacity.low:
        risk_capacity_score += 1
    elif risk_capacity == RiskCapacity.moderate:
        risk_capacity_score += 2
    elif risk_capacity == RiskCapacity.high:
        risk_capacity_score += 3
        
    if risk_tolerance == RiskTolerance.low:
        risk_tolerance_score += 1
    elif risk_tolerance == RiskTolerance.moderate:
        risk_tolerance_score += 2
    elif risk_tolerance == RiskTolerance.high:
        risk_tolerance_score += 3
        
    risk_profile_score = (0.6 * risk_capacity_score) + (0.4 * risk_tolerance_score)
    
    if risk_profile_score < 1.4:
        risk_profile = RiskProfile.very_low
    elif risk_profile_score < 1.8:
        risk_profile = RiskProfile.low
    elif risk_profile_score < 2.2:
        risk_profile = RiskProfile.moderate
    elif risk_profile_score < 2.6:
        risk_profile = RiskProfile.high
    else:
        risk_profile = RiskProfile.very_high
        
    if risk_profile == RiskProfile.very_high and (risk_capacity != RiskCapacity.high or risk_tolerance != RiskTolerance.high):
        risk_profile = RiskProfile.high
    elif risk_profile == RiskProfile.high and (risk_capacity == RiskCapacity.low or risk_tolerance == RiskTolerance.low):
        risk_profile = RiskProfile.moderate
        
    return risk_profile

def generate_profile_explanation(risk_capacity: RiskCapacity, risk_tolerance: RiskTolerance) -> ProfileExplanation:
    return ProfileExplanation(capacity_explanation=CAPACITY_EXPLANATIONS[risk_capacity], tolerance_explanation=TOLERANCE_EXPLANATIONS[risk_tolerance], profile_explanation=PROFILE_EXPLANATIONS[(risk_capacity,risk_tolerance)])

def get_asset_allocation(risk_profile: RiskProfile) -> AssetAllocation:
    return AssetAllocation(**ASSET_ALLOCATIONS[risk_profile])

def get_portfolio_allocation(asset_allocation: AssetAllocation) -> PortfolioAllocation:
    us_stocks = asset_allocation.stocks * US_STOCK_WEIGHT
    international_stocks = asset_allocation.stocks * INTERNATIONAL_STOCK_WEIGHT
    us_bonds = asset_allocation.bonds * US_BOND_WEIGHT
    international_bonds = asset_allocation.bonds * INTERNATIONAL_BOND_WEIGHT
    cash = asset_allocation.cash
    
    return PortfolioAllocation(
        us_stocks=us_stocks,
        international_stocks=international_stocks,
        us_bonds=us_bonds,
        international_bonds=international_bonds,
        cash=cash
    )