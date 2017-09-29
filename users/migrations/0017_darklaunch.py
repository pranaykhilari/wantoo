# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_auto_20160105_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='DarkLaunch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_tag', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('companies', models.ManyToManyField(related_name='company_features', null=True, to='users.Company', blank=True)),
                ('created_by', models.ForeignKey(related_name='user_created_features', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dark Launch Code',
                'verbose_name_plural': 'Dark Launch Codes',
            },
        ),
    ]
