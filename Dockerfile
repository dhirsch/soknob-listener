# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1  \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.10

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY . .
RUN poetry install --no-dev

EXPOSE 4999

WORKDIR /app/app
# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4999"]
