# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0022_status_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['order']},
        ),
    ]
