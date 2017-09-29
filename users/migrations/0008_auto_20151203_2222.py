# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_company_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email_want',
            field=models.BooleanField(default=False),
        ),
    ]
