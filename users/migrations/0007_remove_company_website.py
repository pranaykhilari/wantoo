# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20151127_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='website',
        ),
    ]
