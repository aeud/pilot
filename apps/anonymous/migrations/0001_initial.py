# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0022_visualization_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedVisualization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_active', models.BooleanField(default=True)),
                ('token', models.UUIDField(editable=False, unique=True, default=uuid.uuid4)),
                ('valid_until', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('visualizations', models.ForeignKey(to='visualizations.Visualization')),
            ],
        ),
    ]
