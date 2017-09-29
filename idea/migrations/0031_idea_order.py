# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0030_auto_20160307_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='order',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='status',
            name='order',
            field=models.FloatField(default=0),
        ),
    ]
