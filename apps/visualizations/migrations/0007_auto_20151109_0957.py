# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0006_auto_20151109_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('options', models.TextField()),
                ('chart_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='visualization',
            name='graph',
            field=models.OneToOneField(to='visualizations.Graph', null=True),
        ),
    ]
