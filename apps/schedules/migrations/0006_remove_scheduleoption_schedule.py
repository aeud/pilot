# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_schedule_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduleoption',
            name='schedule',
        ),
    ]
