# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from users.models import UserDetail, Company
from idea.models import Idea, Status


def add_default_ordering(apps, schema_editor):

    Company = apps.get_model('users', 'Company')
    counter = 0

    for company in Company.objects.all():
        Idea = apps.get_model('idea', 'Idea')
        counter = 0

        print '\n'
        print('* Running migration for <Company \"', company.title, '\" with <', Idea.objects.filter(company=company).count(), '> ideas...')

        print '#### GENERATING ORDER FOR IDEAS ####'
        for idea in Idea.objects.filter(company=company).order_by('created_at'):
            idea.order = counter * 65536
            idea.save()
            counter += 1

            print('=> ', idea.title, ' now has order <', idea.order, '>')
        print 'Done...'

        Status = apps.get_model('idea', 'Status')
        counter = 0

        print '\n----------'
        print '#### GENERATING ORDER FOR STATUSES ####'
        for status in Status.objects.filter(company=company).order_by('id'):
            status.order = counter * 65536
            status.save()
            counter += 1

            print('=> ', status.title, ' now has order <', status.order, '>')
        print 'Done...'


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0031_idea_order'),
    ]

    operations = [
    	migrations.RunPython(add_default_ordering),
    ]
