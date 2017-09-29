# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0018_auto_20151126_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='tweet',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
