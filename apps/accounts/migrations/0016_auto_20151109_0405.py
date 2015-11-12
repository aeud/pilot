# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20151109_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bigqueryproject',
            name='created_by',
        ),
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.ForeignKey(to='accounts.Account', default=2),
            preserve_default=False,
        ),
    ]
