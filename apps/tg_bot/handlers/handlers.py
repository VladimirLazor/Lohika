import datetime

import telegram
from django.utils import timezone

from apps.users.models import User
from core.static_text import message_is_sent, help_text
from core.static_text import unlock_secret_room
from core.utils import extract_user_data_from_update
from tg_bot.handlers.manage_data import CONFIRM_BROADCAST
from tg_bot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST
from tg_bot.handlers.utils import handler_logging
from tg_bot.tasks import broadcast_message


@handler_logging()
def help_cmd(update, context):  # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'help after /start command"""
    user_id = extract_user_data_from_update(update)['external_user_id']
    text = help_text

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@handler_logging()
def secret_level(update, context):  # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['external_user_id']
    text = unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(modified__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def broadcast_decision_handler(update,
                               context):  # callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    text = update.callback_query.message.text
    if broadcast_decision == CONFIRM_BROADCAST:
        admin_text = f"{message_is_sent}"
        user_ids = list(User.objects.all().values_list('external_user_id', flat=True))
        broadcast_message.delay(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == CONFIRM_BROADCAST else entities
    )
