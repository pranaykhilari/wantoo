# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20151126_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='notify_comments',
        ),
        migrations.RemoveField(
            model_name='member',
            name='notify_wants',
        ),
        migrations.AddField(
            model_name='member',
            name='email_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='member',
            name='email_comment_on_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='member',
            name='email_comment_on_want',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='member',
            name='email_want',
            field=models.BooleanField(default=True),
        ),
    ]
