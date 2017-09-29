# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0024_auto_20151203_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='color',
            field=models.CharField(default=b'666666', max_length=7),
        ),
    ]
