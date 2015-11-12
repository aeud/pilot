# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0002_dashboardentity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardentity',
            name='position',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dashboardentity',
            name='size',
            field=models.IntegerField(),
        ),
    ]
