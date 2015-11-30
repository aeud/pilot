# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_user_can_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_schedule',
            field=models.BooleanField(default=False),
        ),
    ]
