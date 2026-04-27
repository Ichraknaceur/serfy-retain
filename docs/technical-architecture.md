# Technical Architecture

## Principe

L'architecture conserve la stack existante, mais avec une separation plus nette entre:

- application,
- modeles,
- suivi d'experimentation,
- monitoring,
- automatisation.

## Stack retenue

- `FastAPI` pour l'API metier
- `Streamlit` pour la demonstration et les usages metier simples
- `pandas` / `numpy` pour la preparation des donnees
- `scikit-learn` / `LightGBM` pour le modele churn
- `MLflow` pour le tracking
- `DagsHub` pour la centralisation du suivi
- `Docker` / `docker-compose` pour l'execution locale
- `Jenkins` pour l'automatisation CI/CD
- `Evidently` pour le monitoring data/model
- `pytest` pour les tests

## Architecture logique

```text
Streamlit UI
    |
    v
FastAPI Backend
    |
    +--> Prediction service
    +--> Recommendation service
    +--> Model loader
    |
    +--> Model artifacts
    +--> Preprocessor artifacts

Training pipeline
    |
    +--> MLflow tracking
    +--> DagsHub remote tracking

Monitoring pipeline
    |
    +--> Evidently reports

Automation
    |
    +--> Jenkins pipeline
```

## Structure cible du backend

```text
backend/app/
├── api/routes/
├── core/
├── schemas/
├── services/
│   ├── prediction.py
│   ├── recommendation.py
│   └── model_registry.py
└── main.py
```

## Structure cible data/ML

```text
data/
├── raw/
├── interim/
├── processed/
└── artifacts/

training/
├── preprocess.py
├── train.py
└── evaluate.py
```

## Decisions de conception

### Decision 1

Le frontend reste en `Streamlit` pour accelerer la livraison du MVP.

### Decision 2

Le backend garde `FastAPI` pour isoler les services prediction/recommandation et faciliter les tests.

### Decision 3

Le suivi d'experimentation passe systematiquement par `MLflow` et `DagsHub` pour eviter de repartir en logique notebook-only.

### Decision 4

La couche IA reste optionnelle au depart pour ne pas retarder la valeur metier du MVP.
