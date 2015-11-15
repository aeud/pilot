# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0019_auto_20151115_0550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('start_at', models.DateTimeField()),
                ('completed_at', models.DateTimeField()),
                ('job_id', models.CharField(max_length=255)),
                ('total_rows', models.IntegerField()),
                ('query_checksum', models.CharField(max_length=32)),
                ('cached_until', models.DateTimeField(null=True)),
                ('cache_url', models.CharField(null=True, max_length=255)),
                ('cache_key', models.CharField(null=True, max_length=255)),
                ('query', models.ForeignKey(to='visualizations.Query')),
            ],
        ),
        migrations.CreateModel(
            name='JobExport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('job', models.ForeignKey(to='jobs.Job')),
            ],
        ),
    ]
