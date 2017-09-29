# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0005_remove_idea_session_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='slug',
            field=models.SlugField(max_length=100, null=True, blank=True),
        ),
    ]
