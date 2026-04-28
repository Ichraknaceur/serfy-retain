# Sprint 0 - Framing and Foundation

## Objective

Sprint 0 is used to lock the product and technical framing of `Serfy Retain` before starting functional development.

The goal is to restart on a clean basis with:

- a clear product vision,
- a focused and realistic MVP,
- a stable target architecture,
- an actionable starting backlog,
- a fixed technical stack.

## Main Decision

The technical stack is kept exactly as is:

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
- optional later: `OpenAI` or `OpenRouter` + `ChromaDB`

## Sprint 0 Deliverables

1. Product positioning and value proposition.
2. Definition of personas and the main use case.
3. MVP scope with what is included and excluded.
4. Reference application and MLOps architecture.
5. Initial `serfy-retain` project structure.
6. Transition plan into Sprint 1.

## Target Personas

- `Bank advisor`
  Uses the tool to quickly identify at-risk customers and choose the best retention action.

- `Retention / CRM manager`
  Tracks at-risk segments and offer recommendations to steer campaigns.

- `Data scientist / ML engineer`
  Trains, tracks, versions, and monitors the churn model.

## Main MVP Use Case

1. A user selects or enters a customer profile.
2. The application computes a churn score.
3. The backend classifies the customer into a risk level.
4. The system proposes 1 to 3 relevant retention offers.
5. The user views the result in a simple interface.

## Out of MVP Scope

- full conversational assistant,
- advanced email personalization,
- mandatory RAG/ChromaDB,
- complex cloud orchestration,
- full multi-role authentication.

## Sprint 0 Definition of Done

Sprint 0 is considered complete if:

- the product has a clear name, promise, and framing,
- the stack is locked,
- the MVP is defined,
- the target architecture is documented,
- the next sprint can start without ambiguity.

## Transition to Sprint 1

Sprint 1 starts with 3 goals:

1. make churn data reliable,
2. rebuild a clean training pipeline,
3. track experiments with `MLflow` and `DagsHub`.
