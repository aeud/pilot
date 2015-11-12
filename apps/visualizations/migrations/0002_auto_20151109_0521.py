# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='visualization',
        ),
        migrations.AddField(
            model_name='visualization',
            name='query',
            field=models.OneToOneField(to='visualizations.Query', null=True),
        ),
    ]
