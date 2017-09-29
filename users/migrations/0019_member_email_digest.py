# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20160205_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='email_digest',
            field=models.BooleanField(default=True),
        ),
    ]
