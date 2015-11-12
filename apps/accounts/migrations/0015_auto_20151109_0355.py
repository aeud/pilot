# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20151109_0353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='project',
            new_name='bq_project',
        ),
        migrations.AlterField(
            model_name='bigqueryproject',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
