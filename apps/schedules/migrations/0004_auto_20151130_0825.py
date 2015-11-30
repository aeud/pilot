# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_auto_20151130_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
