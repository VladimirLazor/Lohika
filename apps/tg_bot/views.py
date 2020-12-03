import json
import logging

from django.http import JsonResponse
from django.views import View

from apps.tg_bot.handlers.dispatcher import TELEGRAM_BOT_USERNAME
from apps.tg_bot.handlers.dispatcher import process_telegram_event
from config.settings import DEBUG

logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again. 
    # Can be fixed with async celery task execution
    @classmethod
    def post(cls, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:  # use celery in production
            process_telegram_event.delay(json.loads(request.body))

        # TODO: there is a great trick to send data in webhook response
        # e.g. remove buttons
        return JsonResponse({'ok': 'POST request processed'})

    @classmethod
    def get(cls, request, *args, **kwargs):  # for debug
        return JsonResponse({'ok': 'Get request processed. But nothing done'})


tg_web_hook = TelegramBotWebhookView.as_view()
