from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from apps.core import static_text
from apps.tg_bot.handlers import manage_data


def make_keyboard_for_start_command():
    buttons = [[
        InlineKeyboardButton(static_text.help_button_text, callback_data=f'{manage_data.HELP_BUTTON}'),
        InlineKeyboardButton(static_text.images_button_text, callback_data=f'{manage_data.IMAGES_BUTTON}'),
    ]]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(static_text.confirm_broadcast,
                             callback_data=f'{manage_data.CONFIRM_DECLINE_BROADCAST}{manage_data.CONFIRM_BROADCAST}'),
        InlineKeyboardButton(static_text.decline_broadcast,
                             callback_data=f'{manage_data.CONFIRM_DECLINE_BROADCAST}{manage_data.DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)
