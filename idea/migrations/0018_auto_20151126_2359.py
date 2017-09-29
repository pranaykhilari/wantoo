# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0017_auto_20151126_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.AlterField(
            model_name='idea',
            name='category',
            field=models.ForeignKey(related_name='category_ideas', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='idea.Category', null=True),
        ),
    ]
