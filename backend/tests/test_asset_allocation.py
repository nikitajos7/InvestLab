import pytest
from pydantic import ValidationError
import backend as InvestmentProfile

@pytest.mark.parametrize("risk_profile,expected", [
    (InvestmentProfile.RiskProfile.very_low, {"stocks": 0.20, "bonds": 0.50, "cash": 0.30}),
    (InvestmentProfile.RiskProfile.low, {"stocks": 0.40, "bonds": 0.50, "cash": 0.10}),
    (InvestmentProfile.RiskProfile.moderate, {"stocks": 0.60, "bonds": 0.35, "cash": 0.05}),
    (InvestmentProfile.RiskProfile.high, {"stocks": 0.80, "bonds": 0.15, "cash": 0.05}),
    (InvestmentProfile.RiskProfile.very_high, {"stocks": 0.95, "bonds": 0.00, "cash": 0.05}),
])
def test_get_asset_allocation(risk_profile, expected):
    allocation = InvestmentProfile.get_asset_allocation(risk_profile)

    assert allocation.stocks == expected["stocks"]
    assert allocation.bonds == expected["bonds"]
    assert allocation.cash == expected["cash"]

@pytest.mark.parametrize("stocks,bonds,cash", [
    (1.1, 0.0, 0.0),
    (-0.1, 0.6, 0.5),
    (0.5, 1.1, 0.0),
    (0.5, -0.1, 0.6),
    (0.5, 0.5, 1.1),
    (0.5, 0.6, -0.1),
])
def test_asset_allocation_rejects_invalid_weights(stocks, bonds, cash):
    with pytest.raises(ValidationError):
        InvestmentProfile.AssetAllocation(stocks=stocks, bonds=bonds, cash=cash)

@pytest.mark.parametrize("stocks,bonds,cash", [
    (0.6, 0.3, 0.2),
    (0.4, 0.3, 0.2),
])
def test_asset_allocation_rejects_invalid_total(stocks, bonds, cash):
    with pytest.raises(ValidationError):
        InvestmentProfile.AssetAllocation(stocks=stocks, bonds=bonds, cash=cash)