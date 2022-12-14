# Generated by Django 3.2.5 on 2022-05-03 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email address')),
                ('fisrt_name', models.CharField(default=None, max_length=20)),
                ('last_name', models.CharField(default=None, max_length=20)),
                ('gender', models.CharField(default=None, max_length=6)),
                ('address', models.CharField(default=None, max_length=150)),
                ('is_health', models.CharField(default=None, max_length=3)),
                ('health_info', models.CharField(default=None, max_length=50)),
                ('registered_as', models.CharField(default=None, max_length=10)),
                ('password', models.CharField(default=None, max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('auth_token', models.CharField(max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
