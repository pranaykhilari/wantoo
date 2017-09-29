# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151110_2320'),
        ('idea', '0011_auto_20151118_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(related_name='company_subscriptions', blank=True, to='users.Company', null=True)),
                ('idea', models.ForeignKey(related_name='idea_subscriptions', blank=True, to='idea.Idea', null=True)),
            ],
        ),
    ]
