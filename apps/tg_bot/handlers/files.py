from hashlib import md5
from pathlib import Path

import telegram
from django.core.files.storage import default_storage
from django.utils.datetime_safe import datetime

from apps.users.models import User

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
    hash_key = md5(str(user_id).encode()).hexdigest()

    dirname_date = datetime.today().strftime("%Y-%m-%d")
    dirname = '/'.join([hash_key, dirname_date])
    file_path = '/'.join([dirname, f'{uniq_id}_{file_name}'])
    file_location = '/'.join([default_storage.location, file_path])

    return file_location


def show_file_id(update, context):
    """ Returns file_id of the attached file/media """
    u = User.get_user(update, context)

    if u.is_admin:
        update_json = update.to_dict()
        file_id = _get_file_id(update_json["message"])
        file = context.bot.getFile(file_id)
        file_location = get_file_location(Path(file.file_path).name, file.file_unique_id, u.external_user_id)

        Path.mkdir(Path(file_location).parent, exist_ok=True, parents=True)
        file.download(file_location)

        message_id = update_json["message"]["message_id"]
        update.message.reply_text(text=f"`{file_id}`",
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_to_message_id=message_id)
