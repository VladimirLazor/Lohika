from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(help_text='File.', max_length=256, upload_to='', verbose_name='File'),
        ),
    ]
