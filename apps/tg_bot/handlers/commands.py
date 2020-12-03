import datetime
import re

import telegram
from django.utils import timezone

from apps.users.models import User
from core import static_text
from core.utils import extract_user_data_from_update
from tg_bot.handlers.keyboard_utils import keyboard_confirm_decline_broadcasting
from tg_bot.handlers.keyboard_utils import make_keyboard_for_start_command
from tg_bot.handlers.utils import handler_logging


@handler_logging()
def command_start(update, context):
    user, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=user.first_name)
    else:
        text = static_text.start_not_created.format(first_name=user.first_name)

    update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())


@handler_logging()
def stats(update, context):
    """ Show help info about all secret admins commands """
    user = User.get_user(update, context)
    if not user.is_admin:
        return

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(modified__gte=timezone.now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text,
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


def broadcast_command_with_message(update, context):
    """ Type /broadcast <some_text>. Then check your message in Markdown format and broadcast to users."""
    user = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['external_user_id']

    if not user.is_admin:
        text = static_text.broadcast_no_access
        markup = None

    else:
        text = f"{update.message.text.replace(f'{static_text.broadcast_command} ', '')}"
        markup = keyboard_confirm_decline_broadcasting()

    try:
        context.bot.send_message(
            text=text,
            chat_id=user_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=markup
        )
    except telegram.error.BadRequest as e:
        place_where_mistake_begins = re.findall(r'offset (\d{1,})$', str(e))
        text_error = static_text.error_with_markdown
        if len(place_where_mistake_begins):
            text_error += f"{static_text.specify_word_with_error}'{text[int(place_where_mistake_begins[0]):].split(' ')[0]}'"
        context.bot.send_message(
            text=text_error,
            chat_id=user_id
        )
