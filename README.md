# Zen Stock Screener

A modern, containerized stock analysis dashboard powered by a Zen Rating–style multi-factor scoring engine.

> **Disclaimer:** This tool provides algorithmic analysis and probability estimates for informational purposes only. It is NOT financial advice. Always consult a licensed financial advisor.

---

## Features

- **Zen Rating Engine** — 5-factor scoring (Momentum, Value, Quality, Growth, Risk) producing a 0–100 composite score
- **Real-time dashboard** — Price charts, RSI, MACD, volume, Bollinger Bands
- **Sentiment analysis** — Analyst consensus, price targets, news sentiment
- **Sector comparison table** — Side-by-side watchlist with sortable columns
- **Probability estimates** — Bull/Bear/Neutral directional probabilities (algorithmic, not financial advice)
- **Dark/Light mode** — Full theme support
- **JSON viewer** — Raw API output with tree/raw toggle and copy button
- **Mock + Real data** — Ships with deterministic mock data; plug in yfinance or paid APIs for live data

---

## Architecture

```
┌─────────────────────┐    ┌─────────────────────────────────┐
│   Next.js Frontend  │───▶│       FastAPI Backend           │
│   (React + Tailwind)│    │  /api/v1/score/{ticker}         │
│   Port: 3000        │    │  /api/v1/fundamentals/{ticker}  │
└─────────────────────┘    │  /api/v1/technicals/{ticker}    │
                           │  /api/v1/sentiment/{ticker}     │
                           │  /api/v1/risk/{ticker}          │
                           │  Port: 8000                     │
                           └────────────┬────────────────────┘
                                        │
                           ┌────────────▼────────────────────┐
                           │        Redis Cache              │
                           │   TTL: 5 min (configurable)     │
                           └─────────────────────────────────┘
```

### Scoring Engine

| Factor     | Weight | Key Signals                                 |
|------------|--------|---------------------------------------------|
| Momentum   | 0–20   | RSI, Price/SMA50, Price/SMA200, MACD, Volume|
| Value      | 0–20   | P/E, P/B, P/S, EV/EBITDA, FCF Yield        |
| Quality    | 0–20   | ROE, ROA, Gross Margin, Op Margin, F-Score  |
| Growth     | 0–20   | Revenue Growth, EPS Growth, FCF Yield       |
| Risk       | 0–20   | Beta, Volatility, Altman Z, Debt/Equity     |
| **Composite** | **0–100** | Sum of all factors + grade (A+→F)     |

---

## Project Structure

```
stock-screener/
├── frontend/                   # Next.js 14 (App Router, TypeScript, Tailwind)
│   ├── src/
│   │   ├── app/               # Next.js pages & layout
│   │   ├── components/        # UI components
│   │   │   ├── Dashboard.tsx  # Main layout
│   │   │   ├── ScoreCard.tsx  # Factor + composite score cards
│   │   │   ├── TrendChart.tsx # Price/RSI/MACD/Volume charts
│   │   │   ├── SectorTable.tsx# Watchlist comparison table
│   │   │   ├── ProbabilityIndicator.tsx
│   │   │   ├── JsonViewer.tsx # Raw JSON output viewer
│   │   │   ├── TickerSearch.tsx
│   │   │   └── ThemeToggle.tsx
│   │   ├── hooks/             # SWR data hooks
│   │   ├── types/             # TypeScript interfaces
│   │   └── utils/             # API client
│   ├── Dockerfile
│   └── package.json
│
├── backend/                   # FastAPI (Python 3.12)
│   ├── app/
│   │   ├── api/routes/        # REST endpoints
│   │   │   ├── score.py       # /score — composite Zen Rating
│   │   │   ├── fundamentals.py
│   │   │   ├── technicals.py
│   │   │   ├── sentiment.py
│   │   │   └── risk.py
│   │   ├── core/config.py     # Pydantic settings
│   │   ├── models/stock.py    # Pydantic response models
│   │   ├── scoring/           # Zen Rating engine
│   │   │   ├── engine.py      # Orchestrator
│   │   │   ├── momentum.py
│   │   │   ├── value.py
│   │   │   ├── quality.py
│   │   │   ├── growth.py
│   │   │   └── risk.py
│   │   └── services/
│   │       ├── mock_data.py   # Deterministic mock data generator
│   │       ├── real_data.py   # yfinance real data adapter
│   │       └── cache.py       # Redis cache wrapper
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── deploy/
│   ├── azure/
│   │   ├── container-apps.bicep     # Azure Container Apps + Redis
│   │   ├── acr.bicep                # Azure Container Registry
│   │   └── github-actions-azure.yml # CI/CD pipeline
│   └── aws/
│       ├── cloudformation.yml        # Full VPC + ECS Fargate stack
│       ├── github-actions-aws.yml    # CI/CD pipeline
│       └── terraform/                # Terraform alternative
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
│
├── docker-compose.yml         # Local dev orchestration
├── .env.example               # Environment variable reference
└── README.md
```

---

## Quick Start (Local)

### Prerequisites
- Docker Desktop 24+
- Docker Compose v2

### 1. Clone & configure

```bash
git clone <repo-url>
cd stock-screener
cp .env.example .env
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

The first build takes ~2–3 minutes. After that:

| Service  | URL                          | Notes                          |
|----------|------------------------------|--------------------------------|
| Frontend | http://localhost:3000        | Dashboard UI                   |
| Backend  | http://localhost:8000        | API                            |
| API Docs | http://localhost:8000/docs   | Swagger UI (auto-generated)    |
| Redis    | localhost:6379               | Cache (internal)               |

### 3. Development (no Docker)

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

---

## API Reference

All endpoints are versioned under `/api/v1`.

### GET `/api/v1/score/{ticker}`
Returns the complete Zen Rating for a ticker.

```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "sector": "Technology",
  "momentum": { "score": 14.2, "percentile": 71, "label": "Positive Momentum", "breakdown": {...} },
  "value":    { "score": 9.1,  "percentile": 45, "label": "Fairly Valued", "breakdown": {...} },
  "quality":  { "score": 16.8, "percentile": 84, "label": "High Quality", "breakdown": {...} },
  "growth":   { "score": 12.3, "percentile": 61, "label": "Strong Growth", "breakdown": {...} },
  "risk":     { "score": 13.1, "percentile": 65, "label": "Low Risk", "breakdown": {...} },
  "composite": {
    "total": 65.5,
    "grade": "B",
    "trend": "bullish",
    "bull_probability": 0.52,
    "bear_probability": 0.23,
    "neutral_probability": 0.25
  }
}
```

### GET `/api/v1/score/?tickers=AAPL,MSFT,GOOGL`
Screen multiple tickers in one call (max 20).

### GET `/api/v1/score/watchlist/defaults`
Returns pre-scored default watchlist (15 large-cap tickers).

### GET `/api/v1/fundamentals/{ticker}`
### GET `/api/v1/technicals/{ticker}`
### GET `/api/v1/sentiment/{ticker}`
### GET `/api/v1/risk/{ticker}`

Full Swagger docs at: `http://localhost:8000/docs`

---

## Environment Variables

| Variable                | Default                          | Description                          |
|-------------------------|----------------------------------|--------------------------------------|
| `ENVIRONMENT`           | `development`                    | App environment                      |
| `DEBUG`                 | `false`                          | Enable debug logging                 |
| `DATA_SOURCE`           | `mock`                           | `mock` or `real` (uses yfinance)     |
| `REDIS_URL`             | `redis://redis:6379/0`           | Redis connection URL                 |
| `REDIS_TTL_SECONDS`     | `300`                            | Cache TTL in seconds                 |
| `ALLOWED_ORIGINS`       | `http://localhost:3000,...`      | CORS allowed origins                 |
| `ALPHA_VANTAGE_KEY`     | _(empty)_                        | Optional: Alpha Vantage API key      |
| `FINNHUB_KEY`           | _(empty)_                        | Optional: Finnhub API key            |
| `NEXT_PUBLIC_API_URL`   | `http://localhost:8000`          | Frontend → Backend URL               |

---

## Enabling Real Data

1. Set `DATA_SOURCE=real` in `.env`
2. Uncomment `yfinance` in `backend/requirements.txt`
3. Rebuild: `docker compose up --build`

The backend falls back to mock data if yfinance fails (network issues, invalid ticker, etc.).

---

## Azure Deployment

### Prerequisites
- Azure CLI + subscription
- Azure Container Registry

### 1. Create ACR

```bash
az group create --name zen-screener-rg --location eastus
az deployment group create \
  --resource-group zen-screener-rg \
  --template-file deploy/azure/acr.bicep
```

### 2. Build & Push images

```bash
ACR=<your-acr-name>.azurecr.io
az acr login --name <your-acr-name>

docker build -t $ACR/zen-backend:latest ./backend
docker build -t $ACR/zen-frontend:latest ./frontend \
  --build-arg NEXT_PUBLIC_API_URL=https://zen-backend-prod.azurecontainerapps.io

docker push $ACR/zen-backend:latest
docker push $ACR/zen-frontend:latest
```

### 3. Deploy Container Apps

```bash
az deployment group create \
  --resource-group zen-screener-rg \
  --template-file deploy/azure/container-apps.bicep \
  --parameters \
    acrLoginServer=$ACR \
    acrUsername=$(az acr credential show --name <your-acr-name> --query username -o tsv) \
    acrPassword=$(az acr credential show --name <your-acr-name> --query passwords[0].value -o tsv)
```

### 4. GitHub Actions CI/CD

Add these secrets to your repo:
- `AZURE_CREDENTIALS` — output of `az ad sp create-for-rbac --sdk-auth`
- `AZURE_ACR_NAME`, `AZURE_ACR_LOGIN_SERVER`, `AZURE_RESOURCE_GROUP`
- `BACKEND_URL`

Copy `deploy/azure/github-actions-azure.yml` to `.github/workflows/azure-deploy.yml`.

---

## AWS Deployment

### Option A: CloudFormation

```bash
# Push images to ECR first
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
docker push $ECR_REGISTRY/zen-backend:latest
docker push $ECR_REGISTRY/zen-frontend:latest

# Deploy stack
aws cloudformation deploy \
  --template-file deploy/aws/cloudformation.yml \
  --stack-name zen-screener-prod \
  --parameter-overrides \
    Environment=prod \
    ECRRegistry=$ECR_REGISTRY \
  --capabilities CAPABILITY_NAMED_IAM
```

### Option B: Terraform

```bash
cd deploy/aws/terraform
cp terraform.tfvars.example terraform.tfvars   # edit as needed
terraform init
terraform plan -var="ecr_registry=$ECR_REGISTRY"
terraform apply
```

### GitHub Actions CI/CD

Add secrets: `AWS_DEPLOY_ROLE_ARN`, `AWS_REGION`, `ECR_REGISTRY`, `BACKEND_URL`.

Copy `deploy/aws/github-actions-aws.yml` to `.github/workflows/aws-deploy.yml`.

---

## Security Notes

- API keys are injected via environment variables, never baked into images
- Non-root users in all containers
- CORS restricted to configured origins
- Input validation on all ticker symbols (alpha-only, max 10 chars)
- Rate limiting configurable via `RATE_LIMIT_PER_MINUTE`
- Security headers set on all frontend responses

---

## Extending the Scoring Engine

Each factor lives in `backend/app/scoring/<factor>.py` and returns:
```python
{"score": float, "breakdown": dict, "percentile": float, "label": str}
```

Add a new factor by:
1. Creating `backend/app/scoring/my_factor.py`
2. Importing and calling it in `engine.py`
3. Adding the factor weight to the composite calculation
4. Adding the field to `models/stock.py` and the frontend `types/stock.ts`

---

## Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Frontend    | Next.js 14, TypeScript, Tailwind CSS, Recharts, SWR |
| Backend     | FastAPI, Pydantic v2, Python 3.12       |
| Cache       | Redis 7                                  |
| Container   | Docker, Docker Compose                   |
| Azure       | Container Apps, ACR, Bicep               |
| AWS         | ECS Fargate, ECR, ALB, CloudFormation, Terraform |
| CI/CD       | GitHub Actions (Azure OIDC / AWS OIDC)  |
