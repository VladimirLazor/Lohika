help_text = """
Вас приветствует бот Stegano_Ukraine!
Этот бот создан для стеганографии в изображениях. Подробнее см. ниже.
- Что умеет бот:
    1. Сохранять изображения (как исходные, так и закодированнные)
    2. Кодировать текст в изображениях
    3. Декодировать текст из изображений

- Список команд:
    1. /start - начало работы с ботом
    2. /stop - остановка бота
    3. /images - вызов списка id изображений
    4. /get_image_raw - получение "сырого" изображения по id из списка
    4. /get_image_encoded - получение закодированного изображения по id из списка
    5. /delete_image - удаление изображения по его id
    6. 
    7. /encode <текст> - кодирование указанного текста в изображение
        (первый пробел после команды указывает на начало текста)
    8. /decode (вместе с картинкой) - декодирование текста из отправляемого изображения
    9. /decode_<id> - декодирование текста по id изображения (из списка изображений)
    
"""

unlock_secret_room = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
                     "*Users*: {user_count}\n" \
                     "*24h active*: {active_24}"

help_button_text = "Help"
github_button_text = "GitHub"
secret_level_button_text = "Secret level🗝"

start_created = "Sup, {first_name}!"
start_not_created = "Welcome back, {first_name}!"

broadcast_command = '/broadcast'

broadcast_no_access = "Sorry, you don't have access to this function."
broadcast_header = "This message will be sent to all users.\n\n"
confirm_broadcast = "Confirm✅"
decline_broadcast = "Decline❌"
message_is_sent = "Message is sent✅\n\n"
declined_message_broadcasting = "Message broadcasting is declined❌\n\n"

error_with_markdown = "Can't parse your text in Markdown style."
specify_word_with_error = " You have mistake with the word "

secret_admin_commands = "⚠️ Secret Admin commands\n" \
                        "/stats - bot stats"
