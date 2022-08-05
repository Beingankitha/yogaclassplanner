# Generated by Django 4.0.3 on 2022-05-16 03:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classcalendar', '0002_yogaclass_attendee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yogaclass',
            name='end_time',
        ),
        migrations.AddField(
            model_name='yogaclass',
            name='timeduration',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
