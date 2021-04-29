from pathlib import Path

import telegram
from django.core.files.storage import default_storage
from django.utils.datetime_safe import datetime

from apps.users.models import Image
from apps.users.models import User
from stegano.lsb import hide

ALL_TG_FILE_TYPES = ["document", "video_note", "voice", "sticker", "audio", "video", "animation", "photo"]


def _get_file_id(m):
    """ extract file_id from message (and file type?) """

    for doc_type in ALL_TG_FILE_TYPES:
        if doc_type in m and doc_type != "photo":
            return m[doc_type]["file_id"]

    if "photo" in m:
        best_photo = m["photo"][-1]
        return best_photo["file_id"]


def get_file_location(file_name: str, uniq_id: str, user_id: int):
    hash_key = User.get_hash(user_id)

    dirname_date = datetime.today().strftime("%Y-%m-%d")
    dirname = '/'.join([hash_key, dirname_date])
    file_path = '/'.join([dirname, f'{uniq_id}_{file_name}'])
    file_location = '/'.join([default_storage.location, file_path])

    return file_location


def save_image(update, context):
    user = User.get_user(update, context)
    update_json = update.to_dict()
    message_id = update_json["message"]["message_id"]

    # if not user.is_admin:
    #     update.message.reply_text(text='Not Allowed!',
    #                               parse_mode=telegram.ParseMode.MARKDOWN,
    #                               reply_to_message_id=message_id)
    #     return

    file_id = _get_file_id(update_json["message"])
    caption = update_json['message'].get('caption', None)
    file = context.bot.getFile(file_id)

    file_location = get_file_location(Path(file.file_path).name, file.file_unique_id, user.external_user_id)
    file_location_path = Path(file_location)
    Path.mkdir(file_location_path.parent, exist_ok=True, parents=True)
    file.download(file_location)

    if caption:
        encoded = hide(file_location_path, caption)
        encoded.save(file_location_path)

    Image.objects.create(user=user, file=file_location, is_empty=not bool(caption))

    update.message.reply_text(text=f"File has been uploaded successfully",
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_to_message_id=message_id)
