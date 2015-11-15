# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0018_jobexport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='query',
        ),
        migrations.RemoveField(
            model_name='jobexport',
            name='job',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='JobExport',
        ),
    ]
