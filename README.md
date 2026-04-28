# Serfy Retain

Serfy Retain is a bank churn prevention product.
The goal is to build a clear, modular, and scalable platform that combines:

- churn risk prediction,
- retention offer recommendations,
- AI-assisted personalization,
- product and data monitoring.

## Why This New Project

The previous folders contain strong building blocks, but also a mix of iterations, paths, tests, and CI/CD logic that makes the project harder to evolve safely.
This new repository is meant to provide a clean foundation with:

- a readable architecture,
- simple conventions,
- a clear backend entry point,
- a lightweight frontend UI,
- dedicated space for monitoring and data.

## Sprint 0 Documentation

The initial framing documents are available in `docs/`:

- [Sprint 0](docs/SPRINT_0.md)
- [Product Brief](docs/product-brief.md)
- [MVP Scope](docs/mvp-scope.md)
- [Technical Architecture](docs/technical-architecture.md)

## Product Positioning

Product name: `Serfy Retain`

Tagline:
`The retention intelligence layer for retail banking.`

Promise:
`Identify at-risk customers, recommend the right action, and industrialize retention workflows.`

## Structure

```text
serfy-retain/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── data/
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── monitoring/
│   └── README.md
├── tests/
│   └── test_health.py
├── .env.example
├── .gitignore
└── docker-compose.yml
```

## Local Run

### Backend

```bash
cd serfy-retain/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd serfy-retain/frontend
pip install -r requirements.txt
streamlit run app.py
```

## Docker Run

```bash
cd serfy-retain
docker compose up --build
```

## Tests

```bash
cd serfy-retain/backend
pip install -r requirements-dev.txt
cd ..
pytest tests -q
```

## Recommended Next Steps

1. Add the customer data schema.
2. Connect the churn model through a `services/prediction.py` module.
3. Add a `services/recommendation.py` module for offers.
4. Add a conversational agent in an isolated module.
5. Write backend tests before extending the routes.
