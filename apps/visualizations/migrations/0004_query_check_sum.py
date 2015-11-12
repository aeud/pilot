# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0003_auto_20151109_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='check_sum',
            field=models.CharField(max_length=32, default='tototo'),
            preserve_default=False,
        ),
    ]
