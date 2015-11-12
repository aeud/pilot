# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_credentialsmodel_flowmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentialsmodel',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flowmodel',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='flowmodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID'),
        ),
    ]
