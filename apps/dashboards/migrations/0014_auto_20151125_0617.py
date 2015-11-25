# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboards', '0013_auto_20151124_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='created_by',
            field=models.ForeignKey(null=True, related_name='creator_dashboard_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='star_users',
            field=models.ManyToManyField(related_name='star_dashboards_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
