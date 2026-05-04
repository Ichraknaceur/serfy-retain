FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements-ml.txt ./requirements-ml.txt
RUN pip install --no-cache-dir -r requirements-ml.txt

COPY training ./training
COPY data ./data

CMD ["python", "-m", "training.train"]
