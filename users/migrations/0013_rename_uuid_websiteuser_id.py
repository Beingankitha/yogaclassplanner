# Generated by Django 4.0.3 on 2022-05-18 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_customeuser_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='websiteuser',
            old_name='uuid',
            new_name='id',
        ),
    ]