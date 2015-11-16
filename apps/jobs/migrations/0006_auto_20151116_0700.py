# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_jobrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='job',
            field=models.ForeignKey(to='jobs.Job'),
        ),
    ]
