from apps.core import static_text
from apps.tg_bot.handlers import manage_data
from apps.tg_bot.tasks import broadcast_message
from apps.users.models import User


def broadcast_decision_handler(update,
                               context):  # callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(manage_data.CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    text = update.callback_query.message.text
    if broadcast_decision == manage_data.CONFIRM_BROADCAST:
        admin_text = f"{static_text.message_is_sent}"
        user_ids = list(User.objects.all().values_list('external_user_id', flat=True))
        broadcast_message.delay(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == manage_data.CONFIRM_BROADCAST else entities
    )
