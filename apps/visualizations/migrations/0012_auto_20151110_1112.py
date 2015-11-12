# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0011_auto_20151110_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='cache_url',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='cached_until',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 10, 11, 12, 7, 446233, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
