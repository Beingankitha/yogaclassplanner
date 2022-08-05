# Generated by Django 3.2.5 on 2022-05-08 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220503_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abdominal', models.BooleanField(default=False)),
                ('back_pain', models.BooleanField(default=False)),
                ('neck', models.BooleanField(default=False)),
                ('hip', models.BooleanField(default=False)),
                ('heart', models.BooleanField(default=False)),
                ('low_blood_pressure', models.BooleanField(default=False)),
                ('arthritis', models.BooleanField(default=False)),
                ('spine', models.BooleanField(default=False)),
                ('knee', models.BooleanField(default=False)),
                ('shoulder', models.BooleanField(default=False)),
                ('asthma', models.BooleanField(default=False)),
                ('epilepsy_brain', models.BooleanField(default=False)),
                ('anxiety_depression', models.BooleanField(default=False)),
                ('respiratory_issues', models.BooleanField(default=False)),
                ('eye', models.BooleanField(default=False)),
                ('kidney', models.BooleanField(default=False)),
                ('high_blood_pressure', models.BooleanField(default=False)),
                ('other_problems', models.BooleanField(default=False)),
                ('other_information', models.CharField(default=None, max_length=150)),
                ('any_old_injury', models.BooleanField(default=False)),
                ('any_old_injury_info', models.CharField(default=None, max_length=150)),
                ('is_yoga_exp', models.BooleanField(default=False)),
                ('yoga_exp_level', models.CharField(default=None, max_length=15)),
                ('user_email', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.websiteuser')),
            ],
        ),
    ]
