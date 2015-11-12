# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0008_dashboard_star_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardentity',
            name='size',
            field=models.CharField(max_length=32),
        ),
    ]
