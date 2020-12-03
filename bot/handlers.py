import pathlib
import random

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from PIL import Image

from db.queries import add_image
from db.queries import add_user
from db.queries import delete_image
from db.queries import delete_user
from db.queries import get_image
from db.queries import get_images
from db.queries import get_user

from utils.dirs import create_dir
from utils.dirs import get_media_path
from utils.dirs import remove_dir
from utils.dirs import create_encode_dir

from utils.image import encode as encode_image
from utils.image import decode as decode_image

from utils.text import encode as encode_text
from utils.text import decode as decode_text


REGISTERED_HANDLERS = []


def register(handler, **options):
    def decorator(function):
        options.update({
            'callback': function
        })
        REGISTERED_HANDLERS.append(handler(**options))

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    return decorator


@register(CommandHandler, **{'command': 'start'})
def _(update, context):
    db = context.bot.db
    user_data = update.effective_user.to_dict()
    add_user(db, user_data)
    create_dir(update.effective_user.id)
    create_encode_dir(update, "Encode")
    update.message.reply_text('Welcome!')


@register(CommandHandler, **{'command': 'stop'})
def _(update, context):
    db = context.bot.db
    delete_user(db, update.effective_user.id)
    remove_dir(update.effective_user.id)
    remove_dir("Encode")
    update.message.reply_text('Stop!')


@register(CommandHandler, **{'command': 'images'})
def _(update, context):
    db = context.bot.db
    user = get_user(db, update.effective_user.id)
    images = get_images(db, user.id)
    update.message.reply_text(f'You already have {len(images)} image(s) with index {[image.id for image in images]}')


@register(CommandHandler, **{'command': 'get_random_image'})
def _(update, context):
    db = context.bot.db
    user = get_user(db, update.effective_user.id)
    images = get_images(db, user.id)
    if not images:
        update.message.reply_text('You don\'t have any images')
        return
    photo = random.choice(images)
    with open(photo.path, 'rb') as file:
        update.message.reply_photo(file)


@register(MessageHandler, **{'filters': Filters.regex(r'^(/get_image_[\d]+)$')})
def _(update, context):
    db = context.bot.db
    user = get_user(db, update.effective_user.id)
    image_id = update.message.text.split('_')[-1]
    image = get_image(db, user.id, image_id)

    if not image:
        update.message.reply_text(f'Image does not exists.')
        return

    with open(image.path, 'rb') as file:
        update.message.reply_photo(file)


@register(MessageHandler, **{'filters': Filters.regex(r'^(/delete_image_[\d]+)$')})
def _(update, context):
    db = context.bot.db
    user = get_user(db, update.effective_user.id)
    image_id = update.message.text.split('_')[-1]
    image = get_image(db, user.id, image_id)
    if image:
        image_path = pathlib.Path(image.path)
        if image_path.exists():
            image_path.unlink()
            delete_image(db, image.id)
        update.message.reply_text(f'Image has been deleted')


@register(MessageHandler, **{'filters': Filters.text})
def _(update, context):
    update.message.reply_text(update.message.text)


@register(MessageHandler, **{'filters': (Filters.document.image | Filters.photo)})
def _(update, context):

    try:
        image = update.message.photo[-1]
    except IndexError:
        image = update.message.document

    text = update.message.caption
    if not text:
        update.message.reply_text("No text in there")
        return

    path = get_media_path(update.effective_user.id)
    # path = get_media_path(f"{update.effective_user.id}_raw")

    file = context.bot.getFile(image.file_id)
    suffix = pathlib.Path(file.file_path).suffix
    file_name = f'{file.file_id.split("-")[-1]}{suffix}'
    file_path = path.joinpath(file_name)

    if not file_path.exists():
        file.download(file_path)
        db = context.bot.db
        user = get_user(db, update.effective_user.id)
        if user:
            image_data = {
                'image_path': str(file_path),
                'user_id': user.id,
                'text': text
            }
            add_image(db, image_data)
    update.message.reply_text('Image!')


@register(MessageHandler, **{'filters': Filters.regex(r'^(/encode_[\d]+)$')})
def _(update, context):
    db = context.bot.db
    user = get_user(db, update.effective_user.id)

    image_id = update.message.text.split('_')[-1]
    image = get_image(db, user.id, image_id)

    binary_text = encode_text(image.text)
    pil_image = Image.open(image.path)

    """
    Send image from new path
    """
    new_image_path = encode_image(pil_image, binary_text, user)

    context.bot.sendPhoto(chat_id=user.external_id, photo=open(new_image_path, "rb"))
