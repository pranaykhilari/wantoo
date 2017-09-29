# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import idea.models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0016_subscription_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='key',
            field=models.CharField(default=idea.models.default_sub_key, max_length=20, unique=True, null=True, blank=True),
        ),
    ]
