# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151109_0241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowmodel',
            name='id',
        ),
        migrations.AddField(
            model_name='flowmodel',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, default=1, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False),
        ),
    ]
