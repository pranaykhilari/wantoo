# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20160708_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
