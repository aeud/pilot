# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0010_auto_20151118_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardredirection',
            name='slug',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
