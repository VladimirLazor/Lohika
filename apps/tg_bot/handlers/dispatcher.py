import telegram
from django.conf import settings
from telegram.ext import CommandHandler
from telegram.ext import Dispatcher
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from config.celery import app
from tg_bot.handlers import commands
from tg_bot.handlers import files


def setup_dispatcher(dp):
    """
    Adding handlers for commands
    """
    dp.add_handler(CommandHandler("help", commands.command_help))

    dp.add_handler(CommandHandler("start", commands.command_start))
    dp.add_handler(CommandHandler("stop", commands.command_stop))

    dp.add_handler(CommandHandler("images", commands.command_images))
    dp.add_handler(CommandHandler("get_image", commands.command_get_image))
    dp.add_handler(CommandHandler("delete_image", commands.command_delete_image))

    dp.add_handler(CommandHandler("encode_image", commands.command_encode_image))
    dp.add_handler(CommandHandler("decode_image", commands.command_decode_image))

    dp.add_handler(MessageHandler(
        Filters.document.category("image/"), files.save_image,
    ))

    # dp.add_handler(CallbackQueryHandler(command_help, pattern=f"^{HELP_BUTTON}"))
    # dp.add_handler(CallbackQueryHandler(command_images, pattern=f"^{IMAGES_BUTTON}"))

    # admin commands
    # dp.add_handler(CommandHandler("admin", admin.admin))
    # dp.add_handler(CommandHandler("stats", admin.stats))

    # dp.add_handler(CallbackQueryHandler(secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))
    #
    # dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))
    # dp.add_handler(CallbackQueryHandler(broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}"))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(settings.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    setup_dispatcher(dp)

    bot_info = telegram.Bot(settings.TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(settings.TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
