# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0009_visualization_is_active'),
        ('dashboards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('size', models.IntegerField(max_length=32)),
                ('dashboard', models.ForeignKey(to='dashboards.Dashboard')),
                ('visualization', models.ForeignKey(to='visualizations.Visualization')),
            ],
        ),
    ]
