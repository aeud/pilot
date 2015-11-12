# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_dashboard_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardRedirection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.CharField(max_length=32, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dashboard', models.ForeignKey(to='dashboards.Dashboard')),
            ],
        ),
    ]
