# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('anonymous', '0003_auto_20151201_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareddashboard',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 12, 3, 5, 45, 7, 54028, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sharedvisualization',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 12, 3, 5, 45, 23, 232958, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
