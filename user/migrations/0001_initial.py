# Generated by Django 3.1.5 on 2021-02-06 10:36

from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=15, unique=True, validators=[user.models.validate_username], verbose_name='Username')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('surname', models.CharField(max_length=20, verbose_name='surname')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=user.models.upload_to, verbose_name='Picture')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[user.models.validate_email], verbose_name='Email Address')),
                ('gender', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Gender')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='auth.group', verbose_name='Group')),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
    ]
