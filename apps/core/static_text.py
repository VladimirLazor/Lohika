help_text = """
Вас приветствует бот Stegano\_Ukraine!
Этот бот создан для стеганографии в изображениях. 
Подробности см. ниже.

- Что умеет бот:
    1. Сохранять изображения (как исходные, так и закодированнные)
    2. Кодировать текст в изображениях
    3. Сохранять закодированные изображения
    4. Отправлять список "сырых"/закодированных изображений
    5. Отправлять изображения по их id в соответствующих списках
    6. Удалять изображения
    7. Декодировать текст из изображений

- Список команд:
    0.  /help - вызов этого меню (информация о боте)
    1.  /start - начало работы с ботом
    2.  /stop - остановка бота
    3.  /images {raw, encoded} 
            - raw - вызов списка id "сырых" изображений
            - encoded - вызов списка id закодированных изображений
    4.  /get\_image <id>.{r,e} 
            - r - получение "сырого" изображения по id из соответствующего списка
            - e - получение закодированного изображения по id из соответствующего списка
    5.  /delete\_image <id>.{r,e} - удаление изображения по его id
    6.  /encode\_image <id> <текст> - кодирование указанного текста в изображение
        (первый пробел после id указывает на начало текста)
    7.  /decode\_image (вместе с картинкой) - декодирование текста из отправляемого изображения
    8.  /decode\_image <id> - декодирование текста по id изображения (из списка изображений)
    
"""

unlock_secret_room = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
                     "*Users*: {user_count}\n" \
                     "*24h active*: {active_24}"

help_button_text = "Help"
images_button_text = "Images"

github_button_text = "GitHub"
secret_level_button_text = "Secret level🗝"

start_created = "Sup, {first_name}!"
start_not_created = "Welcome back, {first_name}!"
stop = "Bye, bye👋"

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
