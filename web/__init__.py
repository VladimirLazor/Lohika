import sqlite3

from aiohttp.web import Application
from aiohttp.web import post
from telegram.ext import Dispatcher

from db.utils import check_db
from .handlers import WebHookHandler


async def init_db(app):
    db = sqlite3.connect(app['db_name'], check_same_thread=False)
    db.row_factory = sqlite3.Row
    check_db(db)
    app['dispatcher'].bot.db = db


async def close_dispatcher(app):
    app['dispatcher'].bot.db.close()
    app['dispatcher'].stop()


async def make_app(dispatcher: Dispatcher) -> Application:
    handler = WebHookHandler(dispatcher)

    app = Application(logger=dispatcher.bot.logger)
    app.add_routes([
        post('/', handler.handle_payload),
    ])

    app['db_name'] = 'database.db'
    app['dispatcher'] = dispatcher

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_dispatcher)

    return app
