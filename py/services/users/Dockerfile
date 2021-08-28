FROM python:3.7.9-alpine3.13 as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# A service name to provide common Docker experiance
ENV SERVICE_NAME=users
ENV SERVICE_PATH=/code/services/${SERVICE_NAME}/
ENV VENV_PATH=${SERVICE_PATH}/.venv
ENV PATH="$VENV_PATH/bin:$PATH"

FROM base as builder
# Use a stable Poetry version
ENV POETRY_VERSION=1.1.8 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $SERVICE_PATH

RUN mkdir /install

# Installing required packages
RUN apk add --no-cache \
    curl \
    gcc \
    g++ \
    libc-dev \
    libffi-dev \
    linux-headers \
    openssl-dev \
    postgresql-dev

# Installing Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Copy dependency sources
COPY services/${SERVICE_NAME}/poetry.lock services/${SERVICE_NAME}/pyproject.toml /code/services/${SERVICE_NAME}/
COPY lib/ /code/lib/

# Installing service dependencies
RUN poetry install --no-root --no-dev

FROM base
WORKDIR ${SERVICE_PATH}

# Installing required packages
RUN apk add --no-cache \
    bash \
    libssl1.1 \
    netcat-openbsd \
    postgresql-libs

COPY services/${SERVICE_NAME}/ ${SERVICE_PATH}
COPY --from=builder $VENV_PATH $VENV_PATH

RUN python -m venv $VENV_PATH

CMD ["gunicorn", "users.wsgi:app", "-b", ":8000"]
