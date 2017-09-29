# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_company_slack_webhook'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slack',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
