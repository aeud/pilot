# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0022_visualization_created_by'),
        ('dashboards', '0014_auto_20151125_0617'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedules', '0008_schedule_show_sum'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardSchedule',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=255)),
                ('time', models.CharField(max_length=255)),
                ('frequency', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('anonymous_link', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('dashboard', models.ForeignKey(to='dashboards.Dashboard')),
            ],
        ),
        migrations.CreateModel(
            name='DashboardScheduleOption',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('option', models.IntegerField()),
                ('schedule', models.ForeignKey(to='schedules.DashboardSchedule')),
            ],
        ),
        migrations.CreateModel(
            name='DashboardScheduleVisualization',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('position', models.IntegerField()),
                ('is_image', models.BooleanField(default=False)),
                ('show_sum', models.BooleanField(default=False)),
                ('visualization', models.ForeignKey(to='visualizations.Visualization')),
            ],
        ),
    ]
