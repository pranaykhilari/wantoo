# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0006_auto_20151107_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
    ]
