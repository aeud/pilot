# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0004_query_check_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='query_checksum',
            field=models.CharField(default=213, max_length=32),
            preserve_default=False,
        ),
    ]
