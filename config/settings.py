import pathlib

__all__ = ['settings']

from utils import read_config


class Settings:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    ROOT_DIR = pathlib.Path(__file__).parents[1]
    CONFIG_PATH = ROOT_DIR.joinpath('config.ini')
    REQUIRED_FIELDS = ['BotToken', 'WebHookUrl']
    CONFIG = read_config(CONFIG_PATH, REQUIRED_FIELDS)
    TOKEN = CONFIG.get(CONFIG.default_section, 'BotToken')
    WEB_HOOK_URL = CONFIG.get(CONFIG.default_section, 'WebHookUrl')
    DEBUG = CONFIG.getboolean(CONFIG.default_section, 'Debug')
    PROXY_URL = ""  # CONFIG.get(CONFIG.default_section, 'ProxyUrl')
    MEDIA = 'media'


settings = Settings()
