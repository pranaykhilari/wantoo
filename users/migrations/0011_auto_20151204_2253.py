# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_member_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='title',
            field=models.CharField(max_length=55, verbose_name=b'Company name'),
        ),
    ]
