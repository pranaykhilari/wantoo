# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151030_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='theme',
        ),
        migrations.AddField(
            model_name='company',
            name='color',
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='logo_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
