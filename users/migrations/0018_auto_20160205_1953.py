# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_darklaunch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='darklaunch',
            name='companies',
            field=models.ManyToManyField(related_name='company_features', to='users.Company', blank=True),
        ),
    ]
