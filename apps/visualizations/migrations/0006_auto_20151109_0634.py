# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0005_job_query_checksum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='check_sum',
            new_name='checksum',
        ),
    ]
