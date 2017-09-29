# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20151203_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='title',
            field=models.CharField(max_length=50, verbose_name=b'Company name'),
        ),
    ]
