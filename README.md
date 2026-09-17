# InvestLab

InvestLab is an educational investing decision-support platform designed to help beginner investors understand their risk profile and make more informed investing decisions.

The project is being built incrementally, starting with investor profiling and expanding toward portfolio construction, market data analysis, backtesting, and AI-powered explanations grounded in calculated financial data.

> **Disclaimer:** InvestLab is an educational project. The current risk-scoring model is a custom heuristic and is not financial advice or an official SEC, FINRA, or financial-institution risk assessment methodology.

## Current Features

- Typed investor questionnaire with Pydantic validation
- Separate risk capacity and risk tolerance scoring
- Guardrails for conflicting risk factors
- Five-level overall investor risk profile
- Human-readable explanations for profile results
- FastAPI endpoint with structured request and response models
- Unit tests for scoring logic, boundaries, and guardrails
- API integration tests for successful requests and invalid input

## How It Works

InvestLab separates an investor's ability to take risk from their willingness to take risk.

```text
Investor Questionnaire
        |
        v
+-------------------+       +-------------------+
|   Risk Capacity   |       |  Risk Tolerance   |
|                   |       |                   |
| Financial ability |       | Willingness to    |
| to take risk      |       | accept risk       |
+---------+---------+       +---------+---------+
          |                           |
          +------------+--------------+
                       |
                       v
              Overall Risk Profile
                       |
                       v
                Profile Explanation
```

### Risk Capacity

Risk capacity estimates how much investment risk a user may be financially positioned to take.

The current model considers:

- investment time horizon
- liquidity needs
- reliance on invested funds

The result is:

- `low`
- `moderate`
- `high`

### Risk Tolerance

Risk tolerance estimates a user's willingness to accept investment risk and market volatility.

The current model considers:

- response to a market decline
- preference for lower risk versus higher growth
- comfort with investment losses

The result is:

- `low`
- `moderate`
- `high`

### Overall Risk Profile

Risk capacity and risk tolerance are combined into a five-level investor profile:

- `very_low`
- `low`
- `moderate`
- `high`
- `very_high`

The current model weights risk capacity at **60%** and risk tolerance at **40%**.

Additional guardrails prevent conflicting capacity and tolerance results from producing an overly aggressive overall profile.

## API

### `POST /profile`

Accepts an investor questionnaire and returns the original questionnaire, calculated risk capacity, calculated risk tolerance, overall risk profile, and profile explanations.

### Example Request

```json
{
  "goal": "retirement",
  "time_horizon_years": 1,
  "liquidity_needs": "low",
  "fund_reliance": "non-essential",
  "market_drop_response": "sell_all",
  "investment_preference": "lower_risk",
  "market_loss_comfort": "very_uncomfortable",
  "experience": "beginner"
}
```

### Example Response

```json
{
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
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Tech Stack

### Current

- Python 3.13
- FastAPI
- Pydantic
- Uvicorn
- pytest
- FastAPI TestClient
- uv

### Planned

- PostgreSQL for persistent application and portfolio data
- Pandas, NumPy, and SciPy for financial analytics
- Market data integrations
- Portfolio construction and asset allocation tools
- Historical portfolio analysis and backtesting
- Next.js and TypeScript frontend
- AI-assisted explanations grounded in InvestLab's calculated data
- Docker and cloud deployment

## Running Locally

Clone the repository:

```bash
git clone https://github.com/nikitajos7/investlab.git
cd investlab/backend
```

Install the dependencies:

```bash
uv sync
```

Start the API:

```bash
uv run uvicorn backend:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run the complete test suite from the `backend` directory:

```bash
uv run pytest -v
```

The current test suite covers:

- risk capacity scoring
- risk capacity boundary conditions
- risk capacity guardrails
- risk tolerance scoring
- risk tolerance boundary conditions
- risk tolerance guardrails
- all risk capacity and risk tolerance combinations for the overall profile
- profile explanation generation
- successful `/profile` API requests
- invalid API request validation

## Roadmap

InvestLab is being developed in stages so each new layer builds on a tested foundation.

### 1. Investor Profiling

**Current**

- Investor questionnaire
- Risk capacity
- Risk tolerance
- Overall risk profile
- Profile explanations
- Request and response validation
- Unit and API integration testing

### 2. Portfolio Construction

Translate investor profiles into educational asset allocation examples and model portfolios.

### 3. Market Data & Analytics

Integrate historical market data and calculate portfolio metrics such as:

- returns
- volatility
- drawdowns
- diversification
- risk-adjusted performance

### 4. Backtesting

Allow users to evaluate how model portfolios would have performed across historical market periods.

### 5. AI Investing Copilot

Add an AI explanation layer that uses InvestLab's calculated investor profile, portfolio analytics, and market data as tools and context.

The AI layer will focus on explaining computed results rather than generating unsupported investment recommendations.

### 6. Full-Stack Application

Build a complete application around the analytics engine, including:

- web interface
- persistent user and portfolio data
- background market data workflows
- containerization
- cloud deployment

## Project Status

InvestLab is under active development.

The current version establishes the investor profiling and API foundation. Portfolio construction and financial analytics are the next major development stages.