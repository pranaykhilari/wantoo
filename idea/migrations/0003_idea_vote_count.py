# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0002_auto_20151028_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
