# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0023_auto_20160628_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=55, null=True, blank=True)),
                ('question', models.CharField(max_length=200, null=True, blank=True)),
                ('url', models.URLField( null=True, blank=True)),
                ('company', models.ForeignKey(related_name='featured_companies', to='users.Company')),
                ('created_by', models.ForeignKey(related_name='user_featured_companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Featured Board',
                'verbose_name_plural': 'Featured Boards',
            },
        ),
    ]
