# Made by @alcortazzo
# v0.5

import logging
import os
import time

from telebot import TeleBot, types

import config
from telegram_saucenao import api_requests, media_processing

bot = TeleBot(config.tgBotToken)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    def send_messages():
        bot.send_message(
            message.chat.id,
            'This <a href="https://github.com/alcortazzo/telegram-saucenao"><b>open source</b></a> '
            'bot provides you with an interface to use <a href="https://saucenao.com/"><b>SauceNAO</b></a>`s '
            "reverse image search engine. \n\n<b>author: @alcortazzo</b>\n"
            '<b>donate <a href="https://telegra.ph/Donate-07-22-2">here</a></b>',
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    send_messages()


def guess_source_from_url(url: str):
    """
    "DeviantArt": "da_id",  # https://deviantart.com/view/515715132
    "Pixiv": "pixiv_id",  # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=4933944
    "Anidb": "anidb_aid",  # https://anidb.net/anime/15341
    "Furaffinity": "fa_id",  # https://www.furaffinity.net/view/38849036
    "Twitter": "tweet_id",  # https://twitter.com/i/web/status/742497834117668864
    "bcy": "bcy_id",  # https://bcy.net/illust/detail/55206
    "FurryNetwork": "fn_id",  # https://furrynetwork.com/artwork/103663
    "Pawoo": "pawoo_id",  # https://pawoo.net/@nez_ebi
    "seiga": "seiga_id",  # https://seiga.nicovideo.jp/seiga/im3917445
    "Sankaku": "sankaku_id",  # https://chan.sankakucomplex.com/post/show/1065498
    """
    sites = {
        'https://www.pixiv.net': 'pixiv',
        'https://deviantart.com': 'DeviantArt',
        'https://www.anidb.net': 'Anidb',
        'https://www.furaffinity.net': 'Furaffinity',
        'https://twitter.com': 'Twitter',
        'https://bcy.net': 'bcy',
        'https://pawoo.net': 'Pawoo',
        'https://seiga.nicovideo.jp': 'Seiga',
        'https://chan.sankakucomplex.com': 'Sankaku',
        'https://gelbooru.com': 'Gelbooru',
        'https://anime-pictures.net': 'AnimePictures',
    }

    for site in sites:
        if url.startswith(site):
            return sites[site]
    return 'UNKNOWN'


@bot.message_handler(content_types=["photo"])
def msg_media(message):
    def send_results(result):
        text_result = ""
        if result["name"]:
            text_result += f"<b>{result['name']}</b>\n\n"
        if result["part"]:
            text_result += f"<b>Part:</b> {result['part']}\n"
        if result["year"]:
            text_result += f"<b>Year:</b> {result['year']}\n"
        if result["time"]:
            text_result += f"<b>Time:</b> {result['time']}\n"

        markup = types.InlineKeyboardMarkup()
        buttons = []
        for url in result["urls"]:
            if (url["url"] or url["source"]) and url["similarity"]:
                buttons.append(
                    types.InlineKeyboardButton(
                        text=f"{url['source'] or guess_source_from_url(url['url'])} - {url['similarity']}%", url=url["url"]
                    )
                )
        if buttons:
            markup.add(buttons[0])
            for i in range(1, len(buttons), 2):
                if i+1 < len(buttons):
                    print('markup add row buttons', i, i+1)
                    markup.row(buttons[i], buttons[i+1])
                else:
                    print('markup add row buttons', i)
                    markup.add(buttons[i])

        bot.send_message(
            message.chat.id,
            text_result,
            parse_mode="HTML",
            reply_markup=markup,
            reply_to_message_id=message.id,
        )

    file_name = str(int(time.time()))
    try:
        bot.send_chat_action(message.chat.id, "typing")

        media_file = media_processing.MediaFile(bot, message, file_name)
        media_file.download_media()
        file = media_file.prepare_file()
        results = api_requests.ApiRequest(message.chat.id, file_name)
        results = results.get_result(file)
        send_results(results)
    except Exception as ex:
        text = f"[{type(ex).__name__}] in msg_media(): {str(ex)}"
        logger.error(text)
    finally:
        delete_media(message.chat.id, file_name)


def delete_media(chat_id, filename):
    try:
        folders = os.listdir(f"./media/")
        files = []
        if str(chat_id) in folders:
            files = os.listdir(f"./media/{chat_id}/")
            if f"{filename}.jpg" in files:
                os.remove(f"./media/{chat_id}/{filename}.jpg")
    except Exception as ex:
        text = f"[{type(ex).__name__}] in delete_media(): {str(ex)}"
        logger.error(text)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler("dev.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    while True:
        try:
            bot.polling(none_stop=True)
        except KeyboardInterrupt as ex:
            exit()
        except Exception as ex:
            text = f"[{type(ex).__name__}] in bot.polling(): {str(ex)}"
            logger.error(text)
            if type(ex).__name__ == "ConnectionError":
                time.sleep(3)
