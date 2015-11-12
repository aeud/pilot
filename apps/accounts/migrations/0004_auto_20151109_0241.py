# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151109_0240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentialsmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='flowmodel',
            name='user',
        ),
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.ForeignKey(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='flowmodel',
            name='id',
            field=models.ForeignKey(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
