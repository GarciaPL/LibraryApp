FROM python:3.13-slim

ENV APP_DIR=/usr/src/app
WORKDIR $APP_DIR

RUN pip install --no-cache-dir poetry
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction

COPY ./app ./app

ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["poetry", "run", "flask", "run"]
