# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0015_job_cache_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='map_script',
            field=models.TextField(null=True),
        ),
    ]
