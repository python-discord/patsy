# Patsy
Our beloved assistant, he only has a few simple tasks here at PyDis, using two halves of a coconut to simulate the hoof-beats of [King Arthur's](https://github.com/python-discord/king-arthur) non-existent horse is not one of them!

![Image of Patsy from Monty Python](https://upload.wikimedia.org/wikipedia/en/thumb/6/6a/Patsy%2C_Monty_Python_and_the_Holy_Grail.jpeg/220px-Patsy%2C_Monty_Python_and_the_Holy_Grail.jpeg)

## Purpose
[Python](https://github.com/python-discord/bot) will send Patsy message data, including the content, and Patsy will transform and store that data in postgres.

With this data we plan to inspect what topics get asked about often in help channels, along with which ones go un-answered the most.

To be GDPR compliant, Python will also give an opt-out command, which will be stored by Patsy, and will be used to determine which messages to store, and which to drop.

Deleted messages will always be deleted from the data set, regardless of opt-out status.

## Env file
Patsy requires the following environment variables to be present in a `.env` file, found at the project root.

`DATABASE_URL` - A connection string to the postgres database `postgresql://pypatsy:pypatsy@postgres:5432/pypatsy` if using docker-compose in dev. This is also required in dev to [generate migration files](#generating-migration-files).

The following environment variables are only **required in dev**.

`DEV_GUILD_ID` - The ID of the guild you will be testing this with. This is used to determine which users have permission to use certain endpoints.
`DEBUG` - `true` or `false`. Whether to enable debug mode in the service.

## Running patsy locally
Once your `.env` file is setup, you can start this service by running `docker-compose up` in the root directory.
You can test it's running be navigating to `http://127.0.0.1:8000/ping`

## Generating migration files
After setting up your `.env`, start postgres in docker by running `docker-compose up postgres`.

Once postgres has finished starting, open another terminal and run `alembic revision --autogenerate -m "Migration message here."`.

This will create a migration file in the path `alembic_conf/versions`. Make sure to check it over, and fix any flake8 issues.

## Committing
Before committing make sure to run `poetry install` and then `poetry run task precommit` to install the project dependencies and the pre-commit hook.
