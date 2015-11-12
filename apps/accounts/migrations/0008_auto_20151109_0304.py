# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151109_0302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credentialsmodel',
            old_name='user',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='flowmodel',
            old_name='user',
            new_name='id',
        ),
    ]
