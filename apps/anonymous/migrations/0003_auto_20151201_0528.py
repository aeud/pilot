# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboards', '0014_auto_20151125_0617'),
        ('anonymous', '0002_auto_20151201_0456'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedDashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('valid_until', models.DateTimeField(null=True)),
                ('label', models.CharField(null=True, max_length=255)),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
                ('dashboard', models.ForeignKey(to='dashboards.Dashboard')),
            ],
        ),
        migrations.AddField(
            model_name='sharedvisualization',
            name='label',
            field=models.CharField(null=True, max_length=255),
        ),
    ]
