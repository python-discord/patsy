FROM --platform=linux/amd64 python:3.9-slim

# Set pip to have no saved cache
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install -U pip poetry

# Create the working directory
WORKDIR /patsy

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy the source code in last to optimize rebuilding the image
COPY . .

# Run a single uvicorn worker
# Multiple workers are managed by kubernetes, rather than something like gunicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn --proxy-headers patsy.main:app --host 0.0.0.0 --port 8000"]
