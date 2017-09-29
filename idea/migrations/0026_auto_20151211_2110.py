# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0025_auto_20151210_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='status',
            field=models.ForeignKey(related_name='status_activity', blank=True, to='idea.Status', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.ForeignKey(related_name='status_notifications', blank=True, to='idea.Status', null=True),
        ),
    ]
