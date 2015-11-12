# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20151109_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentialsmodel',
            name='id',
        ),
        migrations.DeleteModel(
            name='CredentialsModel',
        ),
    ]
