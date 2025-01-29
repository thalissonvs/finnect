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

COPY ./docker/dev/start.sh /start.sh

RUN sed -i 's/\r$//g' /start.sh \
    && chmod +x /start.sh
