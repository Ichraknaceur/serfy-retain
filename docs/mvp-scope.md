# MVP Scope

## Included in the MVP

- clean churn preprocessing,
- training of a `LightGBM` model,
- tracking through `MLflow`,
- use of `DagsHub` to centralize experiment tracking,
- `FastAPI` API with `health`, `predict`, and `model-info`,
- `Streamlit` interface to test a customer,
- offer recommendations based on business rules,
- local execution with `Docker Compose`,
- a baseline `Jenkins` pipeline,
- initial monitoring reports with `Evidently`,
- critical tests with `pytest`.

## Excluded from the MVP

- full conversational agent,
- rich human feedback loop,
- mandatory RAG engine,
- advanced AI personalization,
- full authentication and authorization,
- multi-team portal.

## Expected MVP Capabilities

### Data Science Side

- load churn data,
- prepare features,
- train a model,
- compare runs,
- store artifacts.

### Application Side

- check backend status,
- score a customer,
- display the prediction,
- expose the model version,
- recommend offers.

### MLOps Side

- reproduce training,
- track metrics,
- monitor reference and current data,
- launch the application locally with minimal friction.

## MVP Success Criterion

A user must be able to launch the project, test a customer, obtain a churn score, see a retention recommendation, and identify which model produced the decision.
