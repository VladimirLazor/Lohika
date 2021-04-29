from random import shuffle

import telegram
from django.conf import settings
from django.contrib.admin import register
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.core.admin import ActionsModelAdmin
from apps.tg_bot.handlers.utils import send_message
from apps.tg_bot.tasks import broadcast_message
from apps.users.forms import BroadcastForm
from .models import Image
from .models import User
from .models import UserActionLog


@register(User)
class AdminUser(ActionsModelAdmin):
    list_display = (
        'id', 'external_user_id',
        'username', 'get_full_name',
        'language_code', 'deep_link',
        'created', 'is_blocked_bot',
    )
    list_filter = ('is_blocked_bot', 'is_banned', 'is_admin')
    search_fields = ('username', 'external_user_id', 'first_name', 'last_name')
    actions = ['broadcast']

    @staticmethod
    def invited_users(obj):
        return obj.invited_users().count()

    def broadcast(self, request, queryset):
        """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
        if 'apply' in request.POST:
            broadcast_message_text = request.POST['broadcast_text']

            # TODO: for all platforms?
            if len(queryset) <= 3 or settings.DEBUG:  # for test / debug purposes - run in same thread
                for user in queryset:
                    send_message(user_id=user.external_user_id,
                                 text=broadcast_message_text,
                                 parse_mode=telegram.ParseMode.MARKDOWN)
                self.message_user(request, 'Just broadcasted to %d users' % len(queryset))
            else:
                user_ids = list(set(user.external_user_id for user in queryset))
                shuffle(user_ids)
                broadcast_message.delay(message=broadcast_message_text, user_ids=user_ids)
                self.message_user(request, 'Broadcasting of %d messages has been started' % len(queryset))

            return HttpResponseRedirect(request.get_full_path())

        form = BroadcastForm(initial={'_selected_action': queryset.values_list('user_id', flat=True)})

        return render(
            request,
            'admin/broadcast_message.html',
            {'items': queryset, 'form': form, 'title': ''}
        )


@register(UserActionLog)
class AdminUserActionLog(ActionsModelAdmin):
    list_display = ('user', 'action', 'created')


@register(Image)
class Image(ActionsModelAdmin):
    pass
