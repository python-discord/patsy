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

The following environment variables is only **required in production**

`DATABASE_URL` - An asyncpg connection string to the postgres database `postgresql+asyncpg://pypatsy:pypatsy@postgres:5432/pypatsy`.
`STATE_SECRET` - A long random string, must be URL safe.

The following environment variables are only **required in dev**.

`DEBUG` - `true` or `false`. Whether to enable debug mode in the service.

## Running patsy locally
Once your `.env` file is setup, you can start this service by running `docker-compose up` in the root directory.
You can test it's running be navigating to `http://127.0.0.1:8000/ping`

## Generating migration files
With the project running, open another terminal and run ` poetry run task revision "Migration message here."`

This will create a migration file in the path `alembic_conf/versions`. Make sure to check it over, and fix any flake8 issues.

## Committing
Before committing make sure to run `poetry install` and then `poetry run task precommit` to install the project dependencies and the pre-commit hook.
