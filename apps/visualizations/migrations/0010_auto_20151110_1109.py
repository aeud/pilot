# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0009_visualization_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='cached_for',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='query',
            name='cached_until',
            field=models.TimeField(null=True),
        ),
    ]
