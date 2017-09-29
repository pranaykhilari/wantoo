# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_company_blank_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='blank_home',
            field=models.BooleanField(default=False),
        ),
    ]
