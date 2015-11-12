# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20151109_0336'),
    ]

    operations = [
        migrations.CreateModel(
            name='BigQueryProject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('project_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='project_id',
        ),
        migrations.AddField(
            model_name='account',
            name='project',
            field=models.OneToOneField(null=True, to='accounts.BigQueryProject'),
        ),
    ]
