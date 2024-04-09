# Generated by Django 5.0.4 on 2024-04-09 17:12

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import user.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_valid', models.BooleanField(default=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already'}, max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z][a-zA-Z0-9_\\.]+$', 'Enter a valid username')])),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active')),
                ('date_joined', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('last_seen', models.DateTimeField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'users',
                'db_table': 'users',
            },
            managers=[
                ('object', user.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(blank=True, max_length=150)),
                ('avatar', models.ImageField(blank=True, upload_to='profile')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.BooleanField(blank=True, help_text='female is False, male is True, null is unset', null=True)),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.province')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='Divice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_uuid', models.UUIDField(null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('device_type', models.PositiveSmallIntegerField(choices=[(1, 'web'), (2, 'ios'), (3, 'android')], default=3)),
                ('device_os', models.CharField(blank=True, max_length=20)),
                ('device_model', models.CharField(blank=True, max_length=50)),
                ('app_version', models.CharField(blank=True, max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'device',
                'verbose_name_plural': 'devices',
                'unique_together': {('user', 'device_uuid')},
            },
        ),
    ]