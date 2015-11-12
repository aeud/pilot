# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0012_auto_20151110_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='cache_url',
            field=models.CharField(null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='cached_until',
            field=models.DateTimeField(null=True),
        ),
    ]
