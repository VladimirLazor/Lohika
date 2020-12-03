from telegram.bot import Bot


def setup_web_hook(bot: Bot, web_hook_url: str) -> None:
    info = bot.get_webhook_info()

    if info.url == web_hook_url:
        return

    if info.url:
        bot.delete_webhook()

    bot.set_webhook(web_hook_url)
    return
