# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.ForeignKey(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('credential', oauth2client.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlowModel',
            fields=[
                ('id', models.ForeignKey(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('flow', oauth2client.django_orm.FlowField(null=True)),
            ],
        ),
    ]
