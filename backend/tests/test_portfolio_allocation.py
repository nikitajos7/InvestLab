import math

import pytest
from pydantic import ValidationError
import backend as InvestmentProfile


def test_moderate_portfolio_allocation():
    asset_allocation = InvestmentProfile.AssetAllocation(stocks=0.60, bonds=0.35, cash=0.05)
    portfolio = InvestmentProfile.get_portfolio_allocation(asset_allocation)

    assert math.isclose(portfolio.us_stocks, 0.36)
    assert math.isclose(portfolio.international_stocks, 0.24)
    assert math.isclose(portfolio.us_bonds, 0.245)
    assert math.isclose(portfolio.international_bonds, 0.105)
    assert math.isclose(portfolio.cash, 0.05)


@pytest.mark.parametrize("risk_profile", [
    InvestmentProfile.RiskProfile.very_low,
    InvestmentProfile.RiskProfile.low,
    InvestmentProfile.RiskProfile.moderate,
    InvestmentProfile.RiskProfile.high,
    InvestmentProfile.RiskProfile.very_high,
])
def test_portfolio_allocation_pipeline(risk_profile):
    asset_allocation = InvestmentProfile.get_asset_allocation(risk_profile)
    portfolio = InvestmentProfile.get_portfolio_allocation(asset_allocation)

    assert math.isclose(portfolio.us_stocks + portfolio.international_stocks, asset_allocation.stocks)
    assert math.isclose(portfolio.us_bonds + portfolio.international_bonds, asset_allocation.bonds)
    assert math.isclose(portfolio.cash, asset_allocation.cash)
    assert math.isclose(
        portfolio.us_stocks
        + portfolio.international_stocks
        + portfolio.us_bonds
        + portfolio.international_bonds
        + portfolio.cash,
        1.0,
    )


@pytest.mark.parametrize("us_stocks,international_stocks,us_bonds,international_bonds,cash", [
    (1.1, 0.0, 0.0, 0.0, 0.0),
    (-0.1, 0.4, 0.4, 0.2, 0.1),
    (0.3, 1.1, 0.0, 0.0, 0.0),
    (0.3, 0.2, -0.1, 0.5, 0.1),
    (0.3, 0.2, 0.3, 1.1, 0.0),
    (0.3, 0.2, 0.3, 0.2, -0.1),
])
def test_portfolio_allocation_rejects_invalid_weights(us_stocks, international_stocks, us_bonds, international_bonds, cash):
    with pytest.raises(ValidationError):
        InvestmentProfile.PortfolioAllocation(
            us_stocks=us_stocks,
            international_stocks=international_stocks,
            us_bonds=us_bonds,
            international_bonds=international_bonds,
            cash=cash,
        )


@pytest.mark.parametrize("us_stocks,international_stocks,us_bonds,international_bonds,cash", [
    (0.40, 0.20, 0.25, 0.10, 0.10),
    (0.30, 0.20, 0.20, 0.10, 0.10),
])
def test_portfolio_allocation_rejects_invalid_total(us_stocks, international_stocks, us_bonds, international_bonds, cash):
    with pytest.raises(ValidationError):
        InvestmentProfile.PortfolioAllocation(
            us_stocks=us_stocks,
            international_stocks=international_stocks,
            us_bonds=us_bonds,
            international_bonds=international_bonds,
            cash=cash,
        )