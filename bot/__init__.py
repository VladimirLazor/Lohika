from logging import Logger
from queue import Queue
from threading import Thread

from telegram.bot import Bot
from telegram.ext import Dispatcher
from telegram.utils.request import Request

from bot.handlers import REGISTERED_HANDLERS
from bot.utils import setup_web_hook
from config import settings


def setup(token: str,
          web_hook_url: str,
          logger: Logger) -> Dispatcher:
    request = None
    if settings.PROXY_URL:
        request = Request(proxy_url=settings.PROXY_URL)

    bot = Bot(token, request=request)
    bot.logger = logger
    setup_web_hook(bot, web_hook_url)

    update_queue = Queue()

    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    for handler in REGISTERED_HANDLERS:
        dispatcher.add_handler(handler)

    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    return dispatcher
