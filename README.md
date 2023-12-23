# Botami4
Botami is python powerd Telegram bot that allows us to communicate with Tami4 Edge water bar.

## Features
- Boil water.
- Prepare pre-defind drinks.
- Get usage statistics and change dates for the Filter and UB lamp.

## Components and Frameworks used in Botami4
* [Loguru](https://pypi.org/project/loguru/) For logging.
* [pypasser](https://pypi.org/project/PyPasser/) Python library for bypassing reCaptchaV3.
* [Tami4EdgeAPI](https://pypi.org/project/Tami4EdgeAPI/) Tami 4 Edge / Edge+ API in Python.
* [phonenumbers](https://pypi.org/project/phonenumbers/) For Phone numbers verification..
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) - Telegram bot framwork.


## Installation

Before we can start working with Wazy, we need to create a new telegram bot. 

### Create Telegram bot
How to Create a New Bot for Telegram
Open [Telegram messenger](https://web.telegram.org/), sign in to your account or create a new one.

 Enter @Botfather in the search tab and choose this bot (Official Telegram bots have a blue checkmark beside their name.)

[![@Botfather](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")

Click “Start” to activate BotFather bot.

[![@start](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@start")

In response, you receive a list of commands to manage bots.
Choose or type the /newbot command and send it.

[![@newbot](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")


Choose a name for your bot — your subscribers will see it in the conversation. And choose a username for your bot — the bot can be found by its username in searches. The username must be unique and end with the word “bot.”

[![@username](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")


After you choose a suitable name for your bot — the bot is created. You will receive a message with a link to your bot t.me/<bot_username>, recommendations to set up a profile picture, description, and a list of commands to manage your new bot.

[![@bot_username](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")


Botami4 is a docker based application that can be installed using docker compose:

```yaml
version: "3.7"

services:

  botami:
    image: techblog/botami4:latest
    container_name: botami
    restart: always
    environment:
      - BOT_TOKEN=
      - ALLOWD_IDS=
    volumes:
      - ./botami/tokens:/opt/botami/tokens
```

### Environment
* BOT_TOKEN - Token for the TelegramBot.
* ALLOWD_IDS - The telegram Id's allowed to use this bot.


