# Based on
# https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2

import logging
import os
import random
import re

from telegram.ext import CommandHandler, RegexHandler, Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", "5000"))
TOKEN = os.environ.get("TOKEN")


def convert_ft(num):
    result = num * 30.48
    if result < 100:
        return f"{result} cm"
    else:
        return f"{result/100.0} m"


def convert_command(update, context):
    converters = {
        "ft": convert_ft,
        "lbs": lambda num: f"{num * 0.453592} kg",
    }
    try:
        split = update.message.text.split()
        num, unit = split[1:]
        reply = converters[unit](float(num))
    except Exception as e:
        reply = f"write `/convert <NUMBER> <UNIT>` with <UNIT> in on of the following: {', '.join(converters.keys())}\n(error: {e})"
    update.message.reply_text(reply)


def sucks_handler(update, context, groups=None):
    match = context.matches[0].group(0)
    sux = random.choice(
        [
            "sux!",
            "sucks...",
            "sucks ass",
            "is lame!",
            "BOOOOOO!!!!",
            "je sranje :)",
        ]
    )
    update.message.reply_text(f"{match} {sux}!")


def foo_handler(update, context):
    update.message.reply_text("BAR!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    mac_pattern = re.compile(r"(?i)mac")
    dp.add_handler(CommandHandler("convert", callback=convert_command))
    dp.add_handler(RegexHandler("foo", callback=foo_handler))
    dp.add_handler(
        RegexHandler(
            pattern="(?i)mac|win",
            callback=sucks_handler,
            pass_groups=True,
        )
    )
    dp.add_error_handler(error)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://keanu-samurai-bot.herokuapp.com/" + TOKEN)

    updater.idle()


if __name__ == "__main__":
    main()
