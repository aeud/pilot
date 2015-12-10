# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_scheduleoption_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='show_sum',
            field=models.BooleanField(default=False),
        ),
    ]
