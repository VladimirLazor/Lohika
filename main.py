try:
    import uvloop

    use_uvloop = True
except ImportError:
    use_uvloop = False

from aiohttp.web import run_app

from bot import setup
from config import settings
from utils import make_logger
from web import make_app


def main():
    logger = make_logger(settings.DEBUG, name='BotLogger')
    dispatcher = setup(settings.TOKEN, settings.WEB_HOOK_URL, logger)

    run_app(make_app(dispatcher))


if __name__ == '__main__':
    if use_uvloop:
        uvloop.install()
    main()
