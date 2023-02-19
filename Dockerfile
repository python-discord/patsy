FROM --platform=linux/amd64 python:3.11-slim

# Define Git SHA build argument for sentry
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Install project dependencies
WORKDIR /patsy
COPY main-requirements.txt ./
RUN pip install -r main-requirements.txt

# Copy the source code in last to optimize rebuilding the image
COPY . .

EXPOSE 80

# Pull the uvicorn_extra build arg and ave it as an env var.
# The CMD instruction is ran at execution time, so it also needs to be an env var, so that it is available at that time.
ARG uvicorn_extras=""
ENV uvicorn_extras=$uvicorn_extras

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["alembic upgrade head && uvicorn patsy:app --host 0.0.0.0 --port 80 $uvicorn_extras"]
