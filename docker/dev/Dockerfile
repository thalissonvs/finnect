FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential sudo git bash-completion nano ssh \
    libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR ${APP_HOME}

COPY . ${APP_HOME}

RUN pip install poetry
RUN poetry install

COPY ./docker/dev/scripts/start.sh /start.sh
COPY ./docker/dev/scripts/start_celeryworker.sh /start_celeryworker.sh
COPY ./docker/dev/scripts/start_celerybeat.sh /start_celerybeat.sh
COPY ./docker/dev/scripts/start_flower.sh /start_flower.sh

RUN sed -i 's/\r$//g' /start.sh /start_celeryworker.sh /start_celerybeat.sh /start_flower.sh \
    && chmod +x /start.sh /start_celeryworker.sh /start_celerybeat.sh /start_flower.sh
