# Generated by Django 4.0.3 on 2022-05-14 13:27

from django.db import migrations, models
import yogas.models


class Migration(migrations.Migration):

    dependencies = [
        ('yogas', '0014_alter_asana_image_thumbnail_alter_yogaimage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asana',
            name='image_thumbnail',
            field=models.ImageField(default=None, upload_to='media/images/'),
        ),
        migrations.AlterField(
            model_name='yogaimage',
            name='images',
            field=models.FileField(upload_to=yogas.models.content_file_name),
        ),
    ]
