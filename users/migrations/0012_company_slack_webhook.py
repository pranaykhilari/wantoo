# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20151204_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slack_webhook',
            field=models.URLField(max_length=300, null=True, blank=True),
        ),
    ]
