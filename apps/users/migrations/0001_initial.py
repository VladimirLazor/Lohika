import django.utils.timezone
import model_utils.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('external_user_id',
                 models.BigIntegerField(db_index=True, editable=False, help_text='External user_id.', unique=True,
                                        verbose_name='External user_id')),
                ('username',
                 models.CharField(blank=True, db_index=True, default='', help_text='Username.', max_length=32,
                                  verbose_name='Username')),
                ('first_name', models.CharField(help_text='First name.', max_length=256, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, default='', help_text='Last name.', max_length=256,
                                               verbose_name='Last name')),
                ('language_code',
                 models.CharField(blank=True, default='', help_text="Telegram client's lang.", max_length=8,
                                  verbose_name='Language code')),
                ('deep_link',
                 models.CharField(blank=True, db_index=True, default='', help_text='Deep link.', max_length=64,
                                  verbose_name='Deep link')),
                ('is_blocked_bot',
                 models.BooleanField(default=False, help_text='Is blocked bot?', verbose_name='Is blocked bot')),
                ('is_banned', models.BooleanField(default=False, help_text='Is banned?', verbose_name='Is banned')),
                ('is_admin', models.BooleanField(default=False, help_text='Is admin?', verbose_name='Is admin')),
                ('date_joined',
                 models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date joined',
                                      verbose_name='Date joined')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('action', models.CharField(help_text='Action.', max_length=256, verbose_name='Action')),
                ('user', models.ForeignKey(help_text='User.', on_delete=django.db.models.deletion.CASCADE,
                                           related_name='actions_log', to='users.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Action Log',
                'verbose_name_plural': 'Users Actions Log',
                'ordering': ('-created',),
            },
        ),
    ]
