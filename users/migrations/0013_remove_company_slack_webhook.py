# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_company_slack_webhook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='slack_webhook',
        ),
    ]
