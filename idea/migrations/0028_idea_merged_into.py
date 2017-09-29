# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0027_idea_imported'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='merged_into',
            field=models.ForeignKey(blank=True, to='idea.Idea', null=True),
        ),
    ]
