# Telegram-SauceNAO

Telegram-SauceNAO is a Telegram chatbot that uses the SauceNAO image recognition API to identify the source of images sent by users.

## Installation

1. Clone the repository: `git clone https://github.com/kxxoling/Telegram-SauceNAO.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a new Telegram bot and obtain the API token.
4. Create a SauceNAO account and obtain the API key.
5. Export envs like this:

```sh
export TG_BOT_TOKEN=<your_telegram_bot_token>
export SAUCENAO_TOKEN=<your_saucenao_token>
```

6. Start the bot: `python main.py`

## Usage

1. Start a chat with the Telegram bot.
2. Send an image to the bot.
3. The bot will identify the source of the image and reply with the results.

### docker

Run locally:

```sh
docker run --rm -e TG_BOT_TOKEN=xxx -e SAUCENAO_TOKEN=xxx kxxoling/telegram-saucenao
```

Or with docker-compose:

```sh
# Make your own docker-compose.yaml and then run
docker compose up -d
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository. Pull requests are also welcome.

## License

This project is licensed under the GPLv3 License. See the `LICENSE` file for details.

## Credits

Telegram-SauceNAO was created by [alcortazzo](https://github.com/alcortazzo/telegram-saucenao) and maintained by [kxxoling](https://github.com/kxxoling).
The project uses the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) library and the [SauceNAO](https://saucenao.com/) image recognition API.
