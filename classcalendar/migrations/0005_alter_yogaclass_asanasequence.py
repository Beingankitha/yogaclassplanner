# Generated by Django 4.0.3 on 2022-05-16 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yogas', '0020_yogaasanasequence'),
        ('classcalendar', '0004_remove_yogaclass_timeduration_yogaclass_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yogaclass',
            name='asanasequence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='yogas.yogaasanasequence'),
        ),
    ]
