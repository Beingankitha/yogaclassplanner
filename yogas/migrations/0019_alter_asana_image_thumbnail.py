# Generated by Django 4.0.3 on 2022-05-14 21:46

from django.db import migrations, models
import yogas.models


class Migration(migrations.Migration):

    dependencies = [
        ('yogas', '0018_alter_yogaimage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asana',
            name='image_thumbnail',
            field=models.ImageField(default=None, upload_to=yogas.models.content_thumbfile_name),
        ),
    ]
