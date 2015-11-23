# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_userconnection'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_invite',
            field=models.BooleanField(default=False),
        ),
    ]
