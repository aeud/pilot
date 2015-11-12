# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0016_graph_map_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='unstack',
            field=models.BooleanField(default=False),
        ),
    ]
