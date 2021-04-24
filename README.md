# JQBX Bot
A chatbot for JQBX (https://jqbx.fm/) rooms.


## Requirements
* [Python 3.8.6](https://www.python.org/downloads/release/python-386/)
* [pipenv](https://pypi.org/project/pipenv/)
* A Spotify premium account that is already connected to JQBX
* An AWS account to deploy to


## Running Locally
See the `Makefile` for available `make` actions


## Environment Variables
In order for the bot to work, the following environment variables need to be present
(either in the system environment variables, or in a `.env` file in the project root):

| Environment Variable | Description |
| --- | --- |
| DATA_SERVICE_BASE_URL | Base URL of jqbx-bot [data service](https://github.com/jqbx-bot/data-service) (e.g. http://api.com/foo) |
| JQBX_ROOM_ID | The ID of the room that the bot should join. |
| JQBX_BOT_DISPLAY_NAME | The username that the bot should assume in the room |
| JQBX_BOT_IMAGE_URL | A url to an image or gif that the bot should use as its avatar |
| SPOTIFY_USER_ID | The user ID of the JQBX-connected Spotify premium account to be assumed by the bot (NOT including the `spotify:user:` prefix) |
| SPOTIFY_CLIENT_ID | The client ID associated with the Spotify application (for API access) |
| SPOTIFY_CLIENT_SECRET | The client secret associated with the Spotify application (for API access) |
| SPOTIFY_REDIRECT_URI | The redirect URI associated with the Spotify application (for API access) |
| SPOTIFY_REFRESH_TOKEN | The refresh token that will allow the Spotify API to generate new access tokens as needed. See [this article](https://benwiz.com/blog/create-spotify-refresh-token/) for assistance on how to generate. |


## Github Actions
This repository is currently setup to run tests and deploy on each push to `master`

In order for the AWS deployment to succeed, the repository should be configured with the following secrets:

| Secret | Description |
| --- | --- |
| AWS_ACCESS_KEY_ID | Access key ID of an IAM user with sufficient deployment privileges |
| AWS_SECRET_ACCESS_KEY | The secret access key associated with `AWS_ACCESS_KEY_ID` |
| DATA_SERVICE_BASE_URL | Same context as in [Environment Variables](#Environment-Variables) |
| JQBX_ROOM_ID | Same context as in [Environment Variables](#Environment-Variables) |
| JQBX_BOT_DISPLAY_NAME | Same context as in [Environment Variables](#Environment-Variables) |
| JQBX_BOT_IMAGE_URL | Same context as in [Environment Variables](#Environment-Variables) |
| SPOTIFY_USER_ID | Same context as in [Environment Variables](#Environment-Variables) |
| SPOTIFY_CLIENT_ID | Same context as in [Environment Variables](#Environment-Variables) |
| SPOTIFY_CLIENT_SECRET | Same context as in [Environment Variables](#Environment-Variables) |
| SPOTIFY_REDIRECT_URI | Same context as in [Environment Variables](#Environment-Variables) |
| SPOTIFY_REFRESH_TOKEN | Same context as in [Environment Variables](#Environment-Variables) |


## TODO
* implement `/relink` - note to self: "Novastar" by Wrong is area-restricted in the US (as an example to debug with)
