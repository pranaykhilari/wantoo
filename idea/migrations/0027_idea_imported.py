# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0026_auto_20151211_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]
