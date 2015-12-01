# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anonymous', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sharedvisualization',
            old_name='visualizations',
            new_name='visualization',
        ),
    ]
