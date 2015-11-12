# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0010_auto_20151110_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='cached_for',
        ),
        migrations.RemoveField(
            model_name='query',
            name='cached_until',
        ),
        migrations.AddField(
            model_name='visualization',
            name='cached_for',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='visualization',
            name='cached_until',
            field=models.TimeField(null=True),
        ),
    ]
