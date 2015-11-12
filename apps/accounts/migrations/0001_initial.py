# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import apps.accounts.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('email', models.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=254)),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(null=True, max_length=255)),
                ('last_name', models.CharField(null=True, max_length=255)),
                ('handle', models.CharField(unique=True, null=True, max_length=255)),
                ('avatar_url', models.CharField(null=True, max_length=255)),
                ('ga_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.accounts.models.UserManager()),
            ],
        ),
    ]
