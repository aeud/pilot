# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0019_auto_20151115_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='options_is_stacked',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
