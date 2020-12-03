from django.contrib.admin import ModelAdmin
from django.template.loader import render_to_string
from django.urls import path
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.functional import cached_property


class ActionsModelAdmin(ModelAdmin):
    """
    Code were used from https://github.com/lukasvinclav/django-admin-actions
    """
    actions_list = ()
    actions_row = ()
    actions_detail = ()

    @cached_property
    def changelist_admin_url_name(self, lazy=True):
        name = next(filter(lambda x: 'changelist' in x, [p.name for p in self.urls]))
        name = f'admin:{name}'
        if lazy:
            return reverse_lazy(name)
        return name

    def actions_holder(self, instance):
        actions = []

        for method_name in self.actions_row:
            method = getattr(self, method_name)
            actions.append({
                'title': getattr(method, 'short_description', method_name),
                'path': reverse('admin:' + method_name, args=(instance.pk,))
            })

        return render_to_string(
            template_name='admin/change_list_item_object_tools.html',
            context={
                'instance': instance,
                'actions_row': actions,
            })

    actions_holder.short_description = ''

    def get_list_display(self, request):
        if len(self.actions_row) > 0:
            return super().get_list_display(request) + ('actions_holder',)
        return super().get_list_display(request)

    def get_urls(self):
        urls = super().get_urls()

        action_row_urls = []
        for method_name in self.actions_row:
            method = getattr(self, method_name)
            action_row_urls.append(
                path(getattr(method, 'url_path', method_name) + '/<path:pk>/',
                     self.admin_site.admin_view(method),
                     name=method_name))

        action_detail_urls = []
        for method_name in self.actions_detail:
            method = getattr(self, method_name)
            action_detail_urls.append(
                path(getattr(method, 'url_path', method_name) + '/<path:pk>/',
                     self.admin_site.admin_view(method),
                     name=method_name))

        action_list_urls = []
        for method_name in self.actions_list:
            method = getattr(self, method_name)

            action_list_urls.append(
                path(getattr(method, 'url_path', method_name),
                     self.admin_site.admin_view(method),
                     name=method_name))

        return action_list_urls + action_row_urls + action_detail_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}

        actions = []
        for method_name in self.actions_detail:
            method = getattr(self, method_name)

            actions.append({
                'title': getattr(method, 'short_description', method_name),
                'path': reverse('admin:' + method_name, args=(object_id,))
            })

        extra_context.update({
            'actions_list': actions,
        })
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        actions = []
        for method_name in self.actions_list:
            method = getattr(self, method_name)

            actions.append({
                'title': getattr(method, 'short_description', method_name),
                'path': reverse('admin:' + method_name)
            })

        extra_context.update({
            'actions_list': actions,
        })

        return super().changelist_view(request, extra_context)

    class Media:
        css = {
            'all': (
                'css/admin-actions.css',
            )
        }
