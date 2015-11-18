# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0009_auto_20151111_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='slug',
            field=models.CharField(max_length=100),
        ),
    ]
