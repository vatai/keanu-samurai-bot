# Based on
# https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2

import logging
import os

from telegram.ext import CommandHandler, RegexHandler, Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", "5000"))
TOKEN = os.environ.get("TOKEN")


def convert_command(update, context):
    converters = {
        "ft": lambda num: f"{num * 30.48} cm",
        "lbs": lambda num: f"{num * 0.453592} kg",
    }
    try:
        split = update.message.text.split()
        num, unit = split[1:]
        reply = converters[unit](float(num))
    except Exception as e:
        reply = f"write `/convert <NUMBER> <UNIT>` with <UNIT> in on of the following: {', '.join(converters.keys())}\n(error: {e})"
    update.message.reply_text(reply)


def foo_handler(update, context):
    logger.warn(str(update))
    update.message.reply_text("BAR!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("convert", callback=convert_command))
    dp.add_handler(RegexHandler("foo", callback=foo_handler))
    dp.add_error_handler(error)

    updater.start_polling()
    # # Start the Bot
    # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    # # updater.bot.setWebhook("https://yourherokuappname.herokuapp.com/" + TOKEN)
    # updater.bot.setWebhook("https://yourherokuappname.herokuapp.com/" + TOKEN)

    updater.idle()


if __name__ == "__main__":
    main()
