# -*- coding: utf-8 -*-
import sys, os
import datetime

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(THIS_DIR, ".." ))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wantoo.settings'

import django
django.setup()

from users.models import Company, Member
from idea.models import Idea, Comment
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from templated_emails.utils import send_templated_email

now = timezone.now()
seven_days_ago = now - datetime.timedelta(days=7)


send_to = False
if len(sys.argv) > 1 and sys.argv[1] == 'all':
    print 'Sending to all!'
elif len(sys.argv) == 1:
    print 'Use company slug or [all] to send all'
    sys.exit(0)

send_to = sys.argv[1] 


def send_digest_for_company(company):
    print '-----------' 
    print 'Company: ', company.slug
    ideas = Idea.objects.filter(company=company, created_at__gte=seven_days_ago, merged_into__isnull=True)
    if ideas:
        print str(ideas.count()) + ' ideas'
    else:
        print 'No new ideas'
        return

    company_url = ''.join(['https://', get_current_site(None).domain, '/', company.slug, '/'])
    base_url = ''.join(['https://', get_current_site(None).domain, '/'])

    members = Member.objects.filter(company=company)

    for member in members:

        if not member.user.user_detail.email_digest:
            continue

        settings_url = ''.join(['https://', get_current_site(None).domain,'/' + company.slug + '/member/' + str(member.user.id) +'/preferences/notifications/' ])
        try:
            send_templated_email([member.user.email], "emails/digest", {
                'first_name':member.user.first_name,
                'ideas': ideas,
                'company': company,
                'company_url': company_url,
                'user_email': member.user.email,
                'settings_url': settings_url,
                'base_url': base_url,
            }, company.title + ' <noreply+' + company.slug + '@wantoo.io>')       
        except:
            print 'Digest send fail'



if send_to == 'all':
    send_digest_for_company(company_)
    # Send only on Thursdays
    if datetime.datetime.today().weekday() == 3:
        companies = Company.objects.all()

        for company in companies:
            send_digest_for_company(company)
            print company.title
else:
    company = Company.objects.get(slug=send_to)
    send_digest_for_company(company)
