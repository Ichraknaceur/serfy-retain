# MVP Scope

## Inclus dans le MVP

- preprocessing churn propre,
- entrainement d'un modele `LightGBM`,
- tracking via `MLflow`,
- usage de `DagsHub` pour centraliser le suivi,
- API `FastAPI` avec `health`, `predict` et `model-info`,
- interface `Streamlit` pour tester un client,
- recommandations d'offres basees sur des regles metier,
- execution locale via `Docker Compose`,
- pipeline `Jenkins` de base,
- rapports `Evidently` de monitoring initial,
- tests critiques avec `pytest`.

## Exclu du MVP

- agent conversationnel complet,
- boucle de feedback humain riche,
- moteur RAG obligatoire,
- personnalisation IA avancee,
- authentification/autorisation complete,
- portail multi-equipe.

## Capacites MVP attendues

### Cote data science

- charger les donnees churn,
- preparer les features,
- entrainer un modele,
- comparer les runs,
- enregistrer les artefacts.

### Cote applicatif

- verifier l'etat du backend,
- scorer un client,
- afficher la prediction,
- exposer la version du modele,
- recommander des offres.

### Cote MLOps

- reproduire l'entrainement,
- suivre les metriques,
- monitorer les donnees/reference,
- lancer l'application localement facilement.

## Critere de reussite MVP

Un utilisateur doit pouvoir lancer le projet, tester un client, obtenir un score churn, voir une recommandation de retention et identifier quel modele a produit la decision.
