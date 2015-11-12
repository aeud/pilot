# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20151109_0308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowmodel',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='credential',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='FlowModel',
        ),
    ]
