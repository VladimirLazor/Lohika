import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

if __name__ == "__main__":
    from apps.tg_bot.handlers.dispatcher import run_pooling

    run_pooling()
