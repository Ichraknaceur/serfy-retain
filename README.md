# Serfy Retain

Serfy Retain est un produit de prevention du churn bancaire.
L'idee est de construire une plateforme claire, modulaire et evolutive qui combine:

- prediction du risque de churn,
- recommandations d'offres de retention,
- personnalisation assistee par IA,
- monitoring produit et data.

## Pourquoi ce nouveau projet

Les anciens dossiers contiennent de bonnes briques, mais aussi des melanges d'iterations, de chemins, de tests et de CI/CD qui rendent l'evolution plus fragile.
Ce nouveau dossier sert de base propre pour repartir avec:

- une architecture lisible,
- des conventions simples,
- un point d'entree backend clair,
- une UI frontend legere,
- un espace reserve au monitoring et aux donnees.

## Documentation Sprint 0

Les documents de cadrage de depart sont dans `docs/`:

- [Sprint 0](docs/SPRINT_0.md)
- [Product Brief](docs/product-brief.md)
- [MVP Scope](docs/mvp-scope.md)
- [Technical Architecture](docs/technical-architecture.md)

## Positionnement produit

Nom du produit: `Serfy Retain`

Tagline:
`The retention intelligence layer for retail banking.`

Promesse:
`Identifier les clients a risque, recommander la bonne action, et industrialiser la retention.`

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

## Lancement local

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

## Lancement Docker

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

## Prochaines etapes conseillees

1. Ajouter le schema des donnees clients.
2. Brancher le modele churn avec un module `services/prediction.py`.
3. Ajouter un module `services/recommendation.py` pour les offres.
4. Ajouter un agent conversationnel dans un module isole.
5. Ecrire des tests backend avant d'etendre les routes.
