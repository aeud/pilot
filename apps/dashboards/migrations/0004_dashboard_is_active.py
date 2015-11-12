# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0003_auto_20151110_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
