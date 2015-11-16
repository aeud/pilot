# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0006_auto_20151116_0700'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobExportRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('export', models.ForeignKey(to='jobs.JobExport')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='created_by',
            field=models.ForeignKey(default=3, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
