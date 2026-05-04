.DEFAULT_GOAL := help

.PHONY: help build up down logs run-backend run-frontend preprocess-data train-model test mlflow-ui shell-ml

help: ## Show available project commands
	@echo ""
	@echo "Serfy Retain commands"
	@echo "====================="
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

build: ## Build all Docker images
	docker compose build

up: ## Start backend and frontend with Docker Compose
	docker compose up --build backend frontend

down: ## Stop Docker Compose services
	docker compose down

logs: ## Follow Docker Compose logs
	docker compose logs -f

run-backend: ## Start only the backend container
	docker compose up --build backend

run-frontend: ## Start frontend and its backend dependency
	docker compose up --build frontend

preprocess-data: ## Prepare the churn dataset inside the ML container
	docker compose build ml
	docker compose run --rm ml python -m training.preprocess

train-model: ## Train the baseline churn model inside the ML container
	docker compose build ml
	docker compose run --rm ml python -m training.train

test: ## Run the backend test suite inside Docker
	docker compose run --rm backend sh -lc "pip install -r requirements-dev.txt && pytest /app/tests -q"

mlflow-ui: ## Start the local MLflow UI on port 5001
	docker compose up --build mlflow

shell-ml: ## Open a shell inside the ML container
	docker compose run --rm ml sh
