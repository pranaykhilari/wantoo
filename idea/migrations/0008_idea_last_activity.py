# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0007_idea_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='last_activity',
            field=models.ForeignKey(related_name='activity_idea', blank=True, to='idea.Activity', null=True),
        ),
    ]
