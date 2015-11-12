# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20151109_0405'),
        ('dashboards', '0006_dashboardredirection'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardredirection',
            name='account',
            field=models.ForeignKey(to='accounts.Account', default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='slug',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterUniqueTogether(
            name='dashboard',
            unique_together=set([('account', 'slug')]),
        ),
    ]
