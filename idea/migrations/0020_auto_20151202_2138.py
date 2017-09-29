# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_remove_company_website'),
        ('idea', '0019_idea_tweet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=7, null=True, blank=True)),
                ('closed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(related_name='company_statuses', to='users.Company')),
                ('created_by', models.ForeignKey(related_name='user_statuses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.RemoveField(
            model_name='idea',
            name='status',
        ),
        migrations.AlterUniqueTogether(
            name='status',
            unique_together=set([('company', 'title')]),
        ),
    ]
