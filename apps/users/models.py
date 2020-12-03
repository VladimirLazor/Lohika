from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

import ujson as json
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel
from model_utils.models import TimeStampedModel

from apps.core.utils import extract_user_data_from_update


class User(TimeStampedModel,
           SoftDeletableModel):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'external_user_id'
    is_active = True
    is_anonymous = False
    is_authenticated = False
    # region fields
    # region common info
    external_user_id = models.BigIntegerField(
        _('External user_id'),
        editable=False,
        unique=True,
        db_index=True,
        help_text=_('External user_id.'),
    )
    username = models.CharField(
        _('Username'),
        max_length=32,
        db_index=True,
        blank=True,
        default='',
        help_text=_('Username.'),
    )
    first_name = models.CharField(
        _('First name'),
        max_length=256,
        help_text=_('First name.'),
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=256,
        blank=True,
        default='',
        help_text=_('Last name.'),

    )
    language_code = models.CharField(
        _('Language code'),
        max_length=8,
        blank=True,
        default='',
        help_text=_('Telegram client\'s lang.'),
    )
    deep_link = models.CharField(
        _('Deep link'),
        max_length=64,
        db_index=True,
        blank=True,
        default='',
        help_text=_('Deep link.'),

    )
    # endregion

    # region stats
    is_blocked_bot = models.BooleanField(
        _('Is blocked bot'),
        default=False,
        help_text=_('Is blocked bot?'),
    )
    is_banned = models.BooleanField(
        _('Is banned'),
        default=False,
        help_text=_('Is banned?'),
    )
    is_admin = models.BooleanField(
        _('Is admin'),
        default=False,
        help_text=_('Is admin?'),
    )

    # endregion
    date_joined = models.DateTimeField(
        _('Date joined'),
        editable=False,
        default=timezone.now,
        help_text=_('Date joined'),
    )

    # endregion

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return f'@{self.username}' if self.username is not None else f'{self.external_user_id}'

    def get_full_name(self) -> str:
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self) -> str:
        return self.first_name

    def invited_users(self) -> models.QuerySet['User']:  # --> User queryset
        return type(self).objects.filter(
            deep_link=str(self.external_user_id),
            created__gt=self.created,
        )

    @classmethod
    def get_user(cls, update, context) -> 'User':
        user, _ = cls.get_user_and_created(update, context)
        return user

    @classmethod
    def get_user_and_created(cls, update, context) -> Tuple['User', bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        user, created = cls.objects.update_or_create(external_user_id=data['external_user_id'], defaults=data)

        if created:
            try:
                payload = context.args[0]
            except (AttributeError, IndexError):
                pass
            else:
                if str(payload).strip() != str(data['external_user_id']).strip():  # you can't invite yourself
                    user.deep_link = payload
                    user.save(update_fields=('deep_link',))

        return user, created

    @classmethod
    def get_user_by_username_or_user_id(cls, string: str) -> Optional['User']:
        """ Search user in DB, return User or None if not found """
        username = str(string).replace('@', '').strip().lower()
        if username.isdigit():  # external_user_id
            return cls.objects.filter(external_user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()


class UserActionLog(TimeStampedModel):
    # region fields
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='actions_log',
        verbose_name=_('User'),
        help_text=_('User.', )
    )
    action = models.CharField(
        _('Action'),
        max_length=256,
        help_text=_('Action.')
    )

    # endregion
    class Meta:
        verbose_name = _('User Action Log')
        verbose_name_plural = _('Users Actions Log')
        ordering = ('-created',)

    def __str__(self):
        return f"user: {self.user}, made: {self.action}, created at {self.created.strftime('(%H:%M, %d %B %Y)')}"

    @cached_property
    def as_json(self) -> Dict[Any, Any]:
        if not self.action:
            return {}
        try:
            return json.loads(self.action)
        except (TypeError, ValueError):
            return {}
