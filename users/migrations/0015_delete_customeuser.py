# Generated by Django 4.0.3 on 2022-05-23 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_websiteuser_created_at_websiteuser_updated_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomeUser',
        ),
    ]
