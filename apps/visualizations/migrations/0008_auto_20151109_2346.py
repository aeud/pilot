# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0007_auto_20151109_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualization',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
