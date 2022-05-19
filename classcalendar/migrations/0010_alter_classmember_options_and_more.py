# Generated by Django 4.0.3 on 2022-05-17 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_medicalinformation_user_email'),
        ('classcalendar', '0009_classmember'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classmember',
            options={'ordering': ['id']},
        ),
        migrations.AlterUniqueTogether(
            name='classmember',
            unique_together={('yoga_class', 'student')},
        ),
        migrations.DeleteModel(
            name='YogaClassMember',
        ),
    ]
