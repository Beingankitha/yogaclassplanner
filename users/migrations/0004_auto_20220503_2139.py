# Generated by Django 3.2.5 on 2022-05-03 21:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customeuser',
            old_name='is_active',
            new_name='is_verified',
        ),
        migrations.AddField(
            model_name='customeuser',
            name='auth_token',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='customeuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 5, 3, 21, 39, 47, 284572, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
