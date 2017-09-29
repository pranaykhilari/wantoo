# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('idea', '0010_auto_20151112_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=30, choices=[(b'idea_submitted', b'Idea submitted'), (b'comment_added', b'Comment added'), (b'idea_wanted', b'Idea wanted'), (b'joined_community', b'Joined community')])),
                ('seen', models.BooleanField(default=False)),
                ('email_sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='created_notifications', to=settings.AUTH_USER_MODEL)),
                ('idea', models.ForeignKey(related_name='idea_notification', blank=True, to='idea.Idea', null=True)),
                ('user', models.ForeignKey(related_name='user_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='activity',
            name='action',
            field=models.CharField(max_length=30, choices=[(b'idea_submitted', b'Idea submitted'), (b'comment_added', b'Comment added'), (b'idea_wanted', b'Idea wanted'), (b'joined_community', b'Joined community')]),
        ),
    ]
