# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0020_auto_20151202_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='status',
            field=models.ForeignKey(related_name='status_ideas', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='idea.Status', null=True),
        ),
    ]
