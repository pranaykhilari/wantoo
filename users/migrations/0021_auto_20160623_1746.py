# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import Company


def add_group_permissions(apps, schema_editor):

    ct = ContentType.objects.get(app_label='users', model='company')
    permission = Permission.objects.create(codename='is_company_admin', name='Is company admin', content_type=ct)

    Company = apps.get_model('users', 'Company')
    for my_user in Company.objects.all():
        group, created = Group.objects.get_or_create(name=my_user.slug)   
        if created:
            group.permissions.add(permission)
            print  my_user.slug + ' company Group created'


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_company_question'),
    ]

    operations = [
    	migrations.RunPython(add_group_permissions),
    ]


