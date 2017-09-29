# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151028_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'User Membership'},
        ),
        migrations.AlterField(
            model_name='company',
            name='theme',
            field=models.CharField(default=b'black', max_length=15, choices=[(b'black', b'Black'), (b'neutral', b'Neutral'), (b'wantoo', b'wantoo')]),
        ),
    ]
