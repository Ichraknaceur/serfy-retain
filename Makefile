run-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	cd frontend && streamlit run app.py

test:
	pytest tests -q

docker-up:
	docker compose up --build
