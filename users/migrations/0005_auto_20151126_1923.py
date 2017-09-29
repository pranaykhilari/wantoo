# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151110_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='notify_comments',
            field=models.CharField(default=b'instant', max_length=10, choices=[(b'instant', b'Instant'), (b'daily', b'Daily'), (b'never', b'Never')]),
        ),
        migrations.AddField(
            model_name='member',
            name='notify_wants',
            field=models.CharField(default=b'never', max_length=10, choices=[(b'instant', b'Instant'), (b'daily', b'Daily'), (b'never', b'Never')]),
        ),
    ]
