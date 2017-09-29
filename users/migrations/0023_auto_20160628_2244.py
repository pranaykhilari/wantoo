# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0022_auto_20160627_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='darklaunch',
            name='companies',
        ),
        migrations.AddField(
            model_name='darklaunch',
            name='users',
            field=models.ManyToManyField(related_name='user_features', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
