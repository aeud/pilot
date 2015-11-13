# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20151112_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='aws_access_key_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='aws_secret_access_key',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
