import datetime
import re
from pathlib import Path
from shutil import rmtree

import telegram
from django.core.files.storage import default_storage
from django.utils import timezone

from apps.core import static_text
from apps.core.utils import extract_user_data_from_update
from apps.stegano.lsb import hide
from apps.stegano.lsb import reveal
from apps.tg_bot.handlers.files import get_file_location
from apps.tg_bot.handlers.keyboard_utils import keyboard_confirm_decline_broadcasting
from apps.tg_bot.handlers.utils import handler_logging
from apps.users.models import Image
from apps.users.models import User


@handler_logging()
def command_start(update, context):
    user, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=user.first_name)
    else:
        text = static_text.start_not_created.format(first_name=user.first_name)

    update.message.reply_text(text=text)  # , reply_markup=make_keyboard_for_start_command())


@handler_logging()
def command_stop(update, context):
    user_id = extract_user_data_from_update(update)['external_user_id']
    User.all_objects.filter(external_user_id=user_id).delete()
    update.message.reply_text(text=static_text.stop)
    rmtree(default_storage.path(User.get_hash(user_id)), ignore_errors=True)


@handler_logging()
def command_help(update, context):
    user_id = extract_user_data_from_update(update)['external_user_id']
    text = static_text.help_text

    try:
        message_id = update.callback_query.message.message_id
        context.bot.edit_message_text(
            text=text,
            chat_id=user_id,
            message_id=message_id,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    except AttributeError:
        update.message.reply_text(
            text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


@handler_logging()
def command_images(update, context):
    user = User.get_user(update, context)
    try:
        arg = update.message.text.split(' ', maxsplit=1)[-1]
    except AttributeError:
        update.message.reply_text(
            'Something went wrong',
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return
    if arg.startswith('/'):
        arg = 'all'
    elif arg not in ('raw', 'encoded'):
        update.message.reply_text(
            'Invalid image type please use `raw` or `encoded`',
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return
    images_mapper = user.get_ordered_images_mapper(arg)
    text = f"""
    You have {len(images_mapper)} images.
    """
    if len(images_mapper):
        text = f"{text}\nTheir id's is - {', '.join(map(str, images_mapper.keys()))}"

    try:
        message_id = update.callback_query.message.message_id
        context.bot.edit_message_text(
            text=text,
            chat_id=user.external_user_id,
            message_id=message_id,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    except AttributeError:
        update.message.reply_text(
            text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


@handler_logging()
def command_get_image(update, context):
    user = User.get_user(update, context)
    try:
        img_id, img_type, *_ = update.message.text.split(' ', maxsplit=1)[-1].split('.')
        img_id = int(img_id)
        img_type = str(img_type)
        if img_type not in ('r', 'e'):
            update.message.reply_text(
                'Invalid image type please use `r` or `e`',
                parse_mode=telegram.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
            return
    except (ValueError, TypeError, AttributeError,):
        update.message.reply_text(
            'Invalid params',
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    else:
        predicate = 'raw' if img_type == 'r' else 'encoded'
        raw_images = user.get_ordered_images_mapper(predicate)
        if img_id not in raw_images:
            text = f'You dont have {predicate} image with id {img_id}'
            update.message.reply_text(
                text,
                parse_mode=telegram.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
            return
        image = raw_images[img_id]
        text = f'Got Image with db id #{image}'
        update.message.reply_text(
            text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        image = Image.objects.get(id=image)
        update.message.reply_photo(image.file)


@handler_logging()
def command_delete_image(update, context):
    user = User.get_user(update, context)
    try:
        img_id, img_type, *_ = update.message.text.split(' ', maxsplit=1)[-1].split('.')
        img_id = int(img_id)
        img_type = str(img_type)
        if img_type not in ('r', 'e'):
            update.message.reply_text(
                'Invalid image type please use `r` or `e`',
                parse_mode=telegram.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
            return
    except (ValueError, TypeError, AttributeError,):
        update.message.reply_text(
            'Invalid params',
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    else:
        predicate = 'raw' if img_type == 'r' else 'encoded'
        images = user.get_ordered_images_mapper(predicate)
        if img_id not in images:
            text = f'You dont have image with id {img_id}'
        else:
            image = images[img_id]
            image = Image.objects.get(id=image)
            default_storage.delete(image.file.path)
            image.delete()
            text = f'Delete Image {image}'
        update.message.reply_text(
            text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


@handler_logging()
def command_encode_image(update, context):
    user = User.get_user(update, context)
    try:
        img_id, *plain_text = update.message.text.split()[1:]
        img_id = int(img_id)
        plain_text = ' '.join(plain_text)
    except (ValueError, TypeError, AttributeError,):
        update.message.reply_text(
            'Invalid params',
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    else:
        images = user.get_ordered_images_mapper('raw')
        if img_id not in images:
            text = f'You dont have image with id {img_id}'
        else:
            image = Image.objects.get(id=images[img_id])
            encoded_image = hide(image.file, plain_text)
            timestamp = f'encoded-{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}'
            file_location = get_file_location(image.file.name.split('/')[-1], timestamp, user.external_user_id)
            Path.mkdir(Path(file_location).parent, exist_ok=True, parents=True)
            encoded_image.save(file_location)
            Image.objects.create(user=user, file=file_location, is_empty=False)
            text = f'Success'
        update.message.reply_text(
            text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


@handler_logging()
def command_decode_image(update, context):
    user = User.get_user(update, context)
    try:
        img_id, *_ = update.message.text.split()[1:]
        img_id = int(img_id)
    except (ValueError, TypeError, AttributeError,):
        update.message.reply_text(
            'Invalid params',
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    else:
        images = user.get_ordered_images_mapper('encoded')
        if img_id not in images:
            text = f'You dont have image with id {img_id}'
        else:
            image = Image.objects.get(id=images[img_id])
            text = reveal(image.file)
        update.message.reply_text(
            text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


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
