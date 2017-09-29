# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0015_auto_20151119_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='key',
            field=models.CharField(max_length=20, unique=True, null=True, blank=True),
        ),
    ]
