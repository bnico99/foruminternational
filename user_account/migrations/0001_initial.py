# Generated by Django 2.2.7 on 2020-01-14 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=40)),
                ('date_of_birth', models.DateField(null=True)),
                ('signup_confirmation', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('zip_code', models.CharField(max_length=5, null=True)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=30)),
                ('house_number', models.CharField(max_length=10, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('data_privacy', models.BooleanField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]