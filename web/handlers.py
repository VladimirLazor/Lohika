from dataclasses import dataclass
from queue import Queue

from aiohttp.web import Response
from telegram.bot import Bot
from telegram.ext import Dispatcher
from telegram.update import Update


@dataclass
class WebHookHandler:
    bot: Bot
    queue: Queue
    updater: Update = Update

    def __init__(self, dispatcher: Dispatcher) -> None:
        self.bot = dispatcher.bot
        self.queue = dispatcher.update_queue

    async def handle_payload(self, request) -> Response:
        data = await request.json()
        logger = request.app.logger

        update = Update.de_json(data, self.bot)
        logger.debug(update)

        self.queue.put(update)
        return Response()
