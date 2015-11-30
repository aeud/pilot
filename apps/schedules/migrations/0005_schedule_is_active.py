# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0004_auto_20151130_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
