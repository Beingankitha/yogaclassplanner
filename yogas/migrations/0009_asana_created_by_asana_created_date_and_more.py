# Generated by Django 4.0.3 on 2022-05-10 17:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yogas', '0008_auto_20220501_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='asana',
            name='created_by',
            field=models.CharField(default='system', max_length=200),
        ),
        migrations.AddField(
            model_name='asana',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asana',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
