# Patsy
Our beloved assistant, he only has a few simple tasks here at PyDis, using two halves of a coconut to simulate the hoof-beats of [King Arthur's](https://github.com/python-discord/king-arthur) non-existent horse is not one of them!

![Image of Patsy from Monty Python](https://upload.wikimedia.org/wikipedia/en/thumb/6/6a/Patsy%2C_Monty_Python_and_the_Holy_Grail.jpeg/220px-Patsy%2C_Monty_Python_and_the_Holy_Grail.jpeg)

## Purpose
The bot will send Patsy message data, including the content, and Patsy will transform and store that data in postgres. To be GDPR compliant, Patsy will also store the opt-out status of users, and not store data for those users.

## Env file
Patsy requires the following environment variables to be present in a `.env` file, found at the project root.

`CLIENT_ID` - The client ID found in the [Discord API portal](https://discord.com/developers/applications) (Also the user ID of your bot!)

`CLIENT_SECRET` - The OAuth2 client secret, also found in the [Discord API portal](https://discord.com/developers/applications) under the OAuth2 section.

The following environment variables are **required in production**, but not dev as they are set in the docker-compose file.

`REDIRECT_URI` - The callback URI to redirect the user after the Discord OAuth2 flow

`DATABASE_URL` - A connection string to the postgres database

The following environment variable is **required in dev**.

`DEV_GUILD_ID` - The ID of the guild you will be testing this with. This is used to determine which users have permission to use certain endpoints.

## Running patsy locally
Once your `.env` file is setup, you can start this service by running `docker-compose up` in the root directory.
You can test it's running be navigating to `http://127.0.0.1:8000/ping`

## Committing
Before committing make sure to run `poetry install` and then `poetry run precommit` to install the project dependencies and the pre-commit hook
