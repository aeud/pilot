# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0017_query_unstack'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobExport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('job', models.ForeignKey(to='visualizations.Job')),
            ],
        ),
    ]
