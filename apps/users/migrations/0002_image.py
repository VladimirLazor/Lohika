import django.utils.timezone
import model_utils.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('file', models.FilePathField(help_text='File.', max_length=256, verbose_name='File')),
                ('is_empty', models.BooleanField(default=True, help_text='Is Empty?', verbose_name='Is Empty')),
                ('user', models.ForeignKey(help_text='Image.', on_delete=django.db.models.deletion.CASCADE,
                                           related_name='images', to='users.user', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
    ]
