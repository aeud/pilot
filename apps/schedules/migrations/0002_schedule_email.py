# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='email',
            field=models.CharField(default='adrien.eudes@luxola.com', max_length=255),
            preserve_default=False,
        ),
    ]
