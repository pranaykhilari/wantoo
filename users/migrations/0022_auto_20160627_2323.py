# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20160623_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='color',
            field=models.CharField(default=b'3284FF', max_length=7, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo_url',
            field=models.URLField(default=b'http://wantoo.io/static/dashboard/img/company_logos/sample-logo.jpg', null=True, blank=True),
        ),
    ]
