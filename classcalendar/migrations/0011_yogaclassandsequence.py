# Generated by Django 4.0.3 on 2022-05-19 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yogas', '0022_favouriteasana'),
        ('classcalendar', '0010_alter_classmember_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='YogaClassAndSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq_name', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='yogas.yogaasanasequence')),
                ('yoga_class', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='classcalendar.yogaclass')),
            ],
            options={
                'unique_together': {('yoga_class', 'seq_name')},
            },
        ),
    ]
