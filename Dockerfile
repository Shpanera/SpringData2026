FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update     && apt-get install -y --no-install-recommends gcc libpq-dev     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip     && pip install -r /app/requirements.txt

COPY src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/alembic.ini
COPY main.py /app/main.py
COPY run.py /app/run.py
COPY core /app/core

EXPOSE 8000

CMD ["uvicorn", "src.lab6_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
