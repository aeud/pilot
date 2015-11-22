# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0011_auto_20151118_0658'),
        ('jobs', '0007_auto_20151116_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='dashboard',
            field=models.ForeignKey(null=True, to='dashboards.Dashboard'),
        ),
    ]
