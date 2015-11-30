# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visualizations', '0022_visualization_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('time', models.CharField(max_length=255)),
                ('freqency', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('visualization', models.ForeignKey(to='visualizations.Visualization')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('option', models.IntegerField()),
                ('schedule', models.ForeignKey(to='schedules.Schedule')),
            ],
        ),
    ]
