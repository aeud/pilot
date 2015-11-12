# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20151109_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='project_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
