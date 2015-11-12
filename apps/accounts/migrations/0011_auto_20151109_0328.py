# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20151109_0325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='credential',
            new_name='credentials',
        ),
    ]
