# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('idea', '0012_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='company',
        ),
        migrations.AddField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 18, 20, 36, 34, 324065, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='muted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(related_name='user_subscriptions', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='idea',
            field=models.ForeignKey(related_name='idea_subscriptions', default=1, to='idea.Idea'),
            preserve_default=False,
        ),
    ]
