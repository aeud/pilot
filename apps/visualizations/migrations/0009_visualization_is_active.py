# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0008_auto_20151109_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualization',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
