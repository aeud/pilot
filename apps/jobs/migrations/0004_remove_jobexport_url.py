# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobexport_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobexport',
            name='url',
        ),
    ]
