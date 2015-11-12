# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0014_auto_20151110_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='cache_key',
            field=models.CharField(null=True, max_length=255),
        ),
    ]
