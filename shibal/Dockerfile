FROM python:3.11

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.0 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends iputils-ping ffmpeg

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

EXPOSE 8000

COPY . .

CMD ["uvicorn", "--workers", "16", "--host", "0.0.0.0", "--port", "8000", "app_web:app"]
