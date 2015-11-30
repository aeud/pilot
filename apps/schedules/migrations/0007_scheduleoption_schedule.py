# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0006_remove_scheduleoption_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleoption',
            name='schedule',
            field=models.ForeignKey(default=1, to='schedules.Schedule'),
            preserve_default=False,
        ),
    ]
