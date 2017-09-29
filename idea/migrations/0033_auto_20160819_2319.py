# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0032_auto_20160817_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='status',
            field=models.ForeignKey(related_name='status_ideas', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='idea.Status', null=True),
        ),
    ]
