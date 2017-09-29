# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0014_auto_20151119_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(related_name='comment_notifications', blank=True, to='idea.Comment', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='idea',
            field=models.ForeignKey(related_name='idea_notifications', blank=True, to='idea.Idea', null=True),
        ),
    ]
