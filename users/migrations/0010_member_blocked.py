# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20151203_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
