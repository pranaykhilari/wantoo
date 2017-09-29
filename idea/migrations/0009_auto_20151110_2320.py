# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0008_idea_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='last_activity',
            field=models.ForeignKey(related_name='activity_idea', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='idea.Activity', null=True),
        ),
    ]
