# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(related_name='company_members', to='users.Company')),
                ('user', models.ForeignKey(related_name='member_companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Memberships',
            },
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('user', 'company')]),
        ),
    ]
