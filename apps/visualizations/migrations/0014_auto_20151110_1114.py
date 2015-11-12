# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0013_auto_20151110_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visualization',
            old_name='cached_for',
            new_name='cache_for',
        ),
        migrations.RenameField(
            model_name='visualization',
            old_name='cached_until',
            new_name='cache_until',
        ),
    ]
