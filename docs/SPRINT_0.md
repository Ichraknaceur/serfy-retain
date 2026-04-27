# Sprint 0 - Cadrage et fondation

## Objectif

Le Sprint 0 sert a figer le cadre produit et technique de `Serfy Retain` avant de lancer le developpement fonctionnel.

L'objectif est de repartir proprement avec:

- une vision produit claire,
- un MVP limite et realiste,
- une architecture cible stable,
- un backlog de depart exploitable,
- une stack technique figee.

## Decision principale

La stack technique est conservee a l'identique:

- `Python`
- `FastAPI`
- `Streamlit`
- `pandas`
- `numpy`
- `scikit-learn`
- `LightGBM`
- `MLflow`
- `DagsHub`
- `Docker`
- `docker-compose`
- `Jenkins`
- `Evidently`
- `pytest`
- optionnel ensuite: `OpenAI` ou `OpenRouter` + `ChromaDB`

## Livrables Sprint 0

1. Positionnement produit et proposition de valeur.
2. Definition des personas et du cas d'usage principal.
3. Perimetre MVP avec ce qui est inclus et exclu.
4. Architecture applicative et MLOps de reference.
5. Structure initiale du projet `serfy-retain`.
6. Plan de passage vers le Sprint 1.

## Personas cibles

- `Conseiller bancaire`
  Utilise l'outil pour identifier rapidement les clients a risque et choisir la meilleure action de retention.

- `Responsable retention / CRM`
  Suit les segments a risque et les recommandations d'offres pour piloter les campagnes.

- `Data scientist / ML engineer`
  Entraine, suit, versionne et monitore le modele churn.

## Cas d'usage principal MVP

1. Un utilisateur selectionne ou saisit le profil d'un client.
2. L'application calcule un score de churn.
3. Le backend classe le client en niveau de risque.
4. Le systeme propose 1 a 3 offres de retention adaptees.
5. L'utilisateur visualise le resultat dans une interface simple.

## Hors perimetre MVP

- assistant conversationnel complet,
- personnalisation avancée d'emails,
- RAG/ChromaDB obligatoire,
- orchestration cloud complexe,
- authentification multi-role complete.

## Definition of Done du Sprint 0

Le Sprint 0 est considere comme termine si:

- le produit a un nom, une promesse et un cadre clairs,
- la stack est verrouillee,
- le MVP est defini,
- l'architecture cible est documentee,
- le prochain sprint peut commencer sans ambiguite.

## Passage au Sprint 1

Le Sprint 1 demarre avec 3 objectifs:

1. fiabiliser les donnees churn,
2. reconstruire un pipeline d'entrainement propre,
3. tracer les experimentations via `MLflow` et `DagsHub`.
