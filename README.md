# Botami4

Botami is a Python-powered Telegram bot for controlling a Tami4 Edge water bar. From a Telegram chat you can boil water, prepare your saved drinks, and check the filter and UV lamp status, without opening the Tami4 app.

[![Docker Pulls](https://img.shields.io/docker/pulls/techblog/botami4)](https://hub.docker.com/r/techblog/botami4)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](License)

## Table of Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Components and frameworks](#components-and-frameworks)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Using the bot](#using-the-bot)
- [Security notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- Boil water.
- Prepare predefined drinks (the drinks saved on your Tami4 account).
- Get usage statistics and the replacement dates for the filter and UV lamp.
- Log in to your Tami4 account from the bot using your phone number and a one-time password (OTP).
- Restrict the bot to a list of allowed Telegram chat IDs.

## How it works

1. You send your phone number to the bot. The bot asks the Tami4 (Strauss Water) service to send an OTP to that number. The request includes a reCAPTCHA v3 token, which the bot obtains with [PyPasser](https://pypi.org/project/PyPasser/).
2. You send the OTP back to the bot. The bot submits it and receives a **refresh token**, which it saves to `tokens/token.txt`.
3. On later requests the bot reads the refresh token and uses [Tami4EdgeAPI](https://pypi.org/project/Tami4EdgeAPI/) to talk to your water bar (boil, list and prepare drinks, read water quality statistics).

The bot uses long polling, so it does not need an open inbound port or a public URL.

## Components and frameworks

* [Loguru](https://pypi.org/project/loguru/) for logging.
* [PyPasser](https://pypi.org/project/PyPasser/), a Python library for bypassing reCAPTCHA v3.
* [Tami4EdgeAPI](https://pypi.org/project/Tami4EdgeAPI/), a Python API for the Tami4 Edge / Edge+.
* [phonenumbers](https://pypi.org/project/phonenumbers/) for phone number validation.
* [Requests](https://pypi.org/project/requests/) for the OTP requests.
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/), a Telegram bot framework.

## Requirements

- A Tami4 Edge / Edge+ water bar registered to a Tami4 account, and the phone number of that account.
- A Telegram bot token (see [Create a Telegram bot](#create-a-telegram-bot)).
- Your Telegram chat ID.
- Docker and Docker Compose (or Python 3 to run from source).

## Installation

Before we can start working with Botami, we need to create a new Telegram bot.

### Create a Telegram bot

Open [Telegram](https://web.telegram.org/) and sign in to your account, or create a new one.

Enter @BotFather in the search tab and choose this bot (official Telegram bots have a blue checkmark beside their name).

[![@Botfather](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")

Click "Start" to activate the BotFather bot.

[![@start](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")

In response, you receive a list of commands to manage bots.
Choose or type the /newbot command and send it.

[![@newbot](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")

Choose a name for your bot; your subscribers will see it in the conversation. Then choose a username for your bot; the bot can be found by its username in searches. The username must be unique and end with the word "bot".

[![@username](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")

After you choose a suitable name, the bot is created. You will receive a message with a link to your bot (`t.me/<bot_username>`), recommendations for setting up a profile picture and description, and a list of commands to manage your new bot. The message also contains the bot token; you will need it for `BOT_TOKEN`.

[![@bot_username](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")

### Docker Compose

Botami4 is a Docker-based application. The image is published on Docker Hub as [`techblog/botami4`](https://hub.docker.com/r/techblog/botami4) (`linux/amd64`). Install it using Docker Compose:

```yaml
version: "3.7"

services:

  botami:
    image: techblog/botami4:latest
    container_name: botami
    restart: always
    environment:
      - BOT_TOKEN=
      - ALLOWED_IDS=
    volumes:
      - ./botami/tokens:/opt/botami/tokens
```

Fill in `BOT_TOKEN` and `ALLOWED_IDS`, then start the container:

```bash
docker compose up -d
```

### Docker

```bash
docker run -d --name botami --restart always \
  -e BOT_TOKEN=<your-bot-token> \
  -e ALLOWED_IDS=<your-chat-id> \
  -v "$(pwd)/botami/tokens:/opt/botami/tokens" \
  techblog/botami4:latest
```

## Configuration

### Environment

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_TOKEN` | Yes | none | Token of the Telegram bot, from @BotFather. |
| `ALLOWED_IDS` | Yes | Empty in the image (no chat allowed) | The Telegram chat IDs allowed to use this bot. To allow more than one chat, separate the IDs with commas. The value is not parsed or split into a list: the bot checks whether the chat ID appears anywhere in this string, which is why commas work (see [Security notes](#security-notes)). [Here](https://www.alphr.com/telegram-find-user-id/) you can find instructions on how to get your ID. |

### Volumes

| Container path | Description |
|----------------|-------------|
| `/opt/botami/tokens` | To use the Tami4EdgeAPI, a persistent volume should be configured. The Tami4 refresh token is saved in this path as a text file named **token.txt**. Without a volume you have to log in again every time the container is recreated. |

## Using the bot

To start using Botami, open Telegram, go to the bot, and send **/start** or **/help**:

![Main Menu](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/start.png)

The main menu has these buttons:

| Button | Action |
|--------|--------|
| **חידוש / יצירת טוקן** | Create the Tami4 token (phone number + OTP login). Renewing an existing token doesn't work yet; see [Troubleshooting](#troubleshooting). |
| **רשימת משקאות** | Show your saved drinks; tap a drink to prepare it, or **Back ↩** to return to the menu. |
| **סטטיסטיקה ותחזוקה** | Show the filter and UV lamp statistics and replacement dates. |
| **הרתחה** | Boil water. |
| **ביטול** | Close the menu. |

### Log in to Tami4

Click **חידוש / יצירת טוקן**:

![Generate Token](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/token.png)

Next, enter your mobile phone number, including the country code (for example `+972xxxxxxxxx`), to receive the OTP:

![Enter Number](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/phone.png)

Then enter the OTP you received and click "Send":

![Add OTP](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/otp.png)

You can now go back to the main menu by sending **/start** or **/help**:

![Main Menu](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/start.png)

### Statistics

To view the water bar statistics, click **סטטיסטיקה ותחזוקה**:

![Stats Menu](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/stats_menu.png)

The bot replies with the last and next replacement dates and the status of the filter and the UV lamp, and the number of liters that passed through the filter:

![Stats](https://raw.githubusercontent.com/t0mer/Botami4/main/screenshots/stats.png)

## Security notes

- Access control is weak. `ALLOWED_IDS` is a raw string, and the bot checks whether the chat ID appears **anywhere in it** (a substring test), not whether it matches an ID in a list. A chat ID that is part of an allowed ID (for example `123` when `1234` is allowed) is also accepted.
- The drink buttons and the **ביטול** button don't check `ALLOWED_IDS` at all. The menu, token, boil, drinks list and statistics actions do.
- Chats that fail the check get no response.
- The Tami4 refresh token is stored in plain text in `tokens/token.txt`. Anyone with this file can control your water bar, so protect the volume directory and don't commit it or share it.
- Keep `BOT_TOKEN` secret. If it leaks, revoke it with @BotFather (`/revoke`) and update the container.

## Troubleshooting

- **The bot doesn't respond to /start**: check that your chat ID is in `ALLOWED_IDS`. The image default is an empty string, so every chat is rejected until you set it. Rejected chats are ignored silently, and nothing is written to the logs (`docker logs botami`).
- **"Invalid Phone number"**: the number must start with `+` and the country code, for example `+972xxxxxxxxx`.
- **Replacing an existing Tami4 token**: logging in again with **חידוש / יצירת טוקן** reports success but doesn't overwrite an existing `token.txt`, and the running bot keeps the token it already loaded. To replace a token, delete `tokens/token.txt`, restart the container (`docker restart botami`), and then log in again.
- **Buttons do nothing after a restart**: make sure the `tokens` volume is mounted and contains `token.txt`. If it doesn't, log in again with **חידוש / יצירת טוקן**.

## Development

Project layout:

```
botami/botami.py     # the bot
requirements.txt     # Python dependencies
Dockerfile           # container image
docker-compose.yaml  # example Compose file
screenshots/         # README images
```

Run from source:

```bash
pip install -r requirements.txt
cd botami
BOT_TOKEN=<your-bot-token> ALLOWED_IDS=<your-chat-id> python botami.py
```

The refresh token is saved in a `tokens` directory under the current working directory.

Build the image locally:

```bash
docker build -t botami4 .
```

## Contributing

Issues and pull requests are welcome on [GitHub](https://github.com/t0mer/Botami4).

## License

This project is licensed under the Apache License 2.0. See [License](License) for details.
