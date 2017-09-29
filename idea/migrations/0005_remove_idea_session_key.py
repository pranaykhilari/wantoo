# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0004_auto_20151105_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='session_key',
        ),
    ]
