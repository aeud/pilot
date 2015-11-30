# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_schedule_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='freqency',
            new_name='frequency',
        ),
    ]
