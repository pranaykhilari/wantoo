# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0021_idea_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
