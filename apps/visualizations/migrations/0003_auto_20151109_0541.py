# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0002_auto_20151109_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='job',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='job',
            name='completed_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 40, 54, 953526, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='job_id',
            field=models.CharField(default='fasfsaas', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 41, 13, 625901, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='total_rows',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
