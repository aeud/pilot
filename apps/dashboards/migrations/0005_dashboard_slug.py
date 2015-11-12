# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0004_dashboard_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='slug',
            field=models.CharField(default='toto', unique=True, max_length=32),
            preserve_default=False,
        ),
    ]
