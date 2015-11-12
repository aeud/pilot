# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151109_0243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flowmodel',
            old_name='user',
            new_name='id',
        ),
    ]
