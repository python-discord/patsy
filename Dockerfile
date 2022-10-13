FROM --platform=linux/amd64 ghcr.io/chrislovering/python-poetry-base:3.10-slim

ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Create the working directory
WORKDIR /patsy

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# Copy the source code in last to optimize rebuilding the image
COPY . .

EXPOSE 80

# Pull the uvicorn_extra build arg and ave it as an env var.
# The CMD instruction is ran at execution time, so it also needs to be an env var, so that it is available at that time.
ARG uvicorn_extras=""
ENV uvicorn_extras=$uvicorn_extras

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["poetry run alembic upgrade head && poetry run uvicorn patsy:app --host 0.0.0.0 --port 80 $uvicorn_extras"]
