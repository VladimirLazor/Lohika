import datetime

import telegram
from django.utils.timezone import now

from core import static_text
from apps.users.models import User


def admin(update, context):
    """ Show help info about all secret admins commands """
    user = User.get_user(update, context)
    if not user.is_admin:
        return

    return update.message.reply_text(static_text.secret_admin_commands)


def stats(update, context):
    """ Show help info about all secret admins commands """
    user = User.get_user(update, context)
    if not user.is_admin:
        return

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(modified__gte=now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text,
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
