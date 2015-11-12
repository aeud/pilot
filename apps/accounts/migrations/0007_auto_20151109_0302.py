# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151109_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credentialsmodel',
            old_name='id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='flowmodel',
            old_name='id',
            new_name='user',
        ),
    ]
