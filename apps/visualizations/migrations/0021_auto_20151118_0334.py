# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0020_graph_options_is_stacked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='options_is_stacked',
            field=models.CharField(max_length=255, default='false'),
            preserve_default=False,
        ),
    ]
