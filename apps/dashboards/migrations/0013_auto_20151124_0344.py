# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0012_dashboardrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
