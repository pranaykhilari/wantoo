# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0028_idea_merged_into'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='keywords',
            field=models.TextField(null=True, blank=True),
        ),
    ]
