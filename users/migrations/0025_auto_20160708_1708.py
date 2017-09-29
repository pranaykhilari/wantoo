# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_featurecompany'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='email_comment',
        ),
        migrations.RemoveField(
            model_name='member',
            name='email_comment_on_comment',
        ),
        migrations.RemoveField(
            model_name='member',
            name='email_comment_on_want',
        ),
        migrations.RemoveField(
            model_name='member',
            name='email_digest',
        ),
        migrations.RemoveField(
            model_name='member',
            name='email_want',
        ),
        migrations.AddField(
            model_name='userdetail',
            name='email_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='email_comment_on_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='email_comment_on_want',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='email_digest',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='email_want',
            field=models.BooleanField(default=False),
        ),
    ]
