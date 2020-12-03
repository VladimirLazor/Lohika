from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from core.static_text import confirm_broadcast, help_button_text
from core.static_text import decline_broadcast
from core.static_text import secret_level_button_text
from tg_bot.handlers.manage_data import HELP_BUTTON
from tg_bot.handlers.manage_data import CONFIRM_BROADCAST
from tg_bot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST
from tg_bot.handlers.manage_data import DECLINE_BROADCAST


def make_keyboard_for_start_command():
    buttons = [[
        InlineKeyboardButton(help_button_text, callback_data=f'{HELP_BUTTON}'),
    ]]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(confirm_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{CONFIRM_BROADCAST}'),
        InlineKeyboardButton(decline_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)
