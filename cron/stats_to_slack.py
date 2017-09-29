# -*- coding: utf-8 -*-
import sys, os, csv
import datetime
import requests
import json

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(THIS_DIR, ".." ))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wantoo.settings'

import django
django.setup()

from users.models import Company, Member
from idea.models import Idea, Comment
from django.db.models import Q
from django.utils import timezone
from django.contrib.sites.models import get_current_site


slack_webhook = "https://hooks.slack.com/services/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" 
# slack_webhook = "https://hooks.slack.com/services/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" #erinc channel

payload = {
    "username": "wantoo",
    "mrkdwn": True,
    "icon_url": "http://wantoo.io/wp-content/uploads/2015/02/favicon.png"
}

companies = Company.objects.all().order_by('created_at')
attachments = []
for c in companies:
    a = {}

    company_url = ''.join(['https://', get_current_site(None).domain, '/' + c.slug + '/' ])
    a['pretext'] = "*<%s|%s>*" % (company_url, c.title)

    if c.color:
        a['color'] = "#" + c.color
    else:
        a['color'] = "#fb1fb4"

    a['fields'] = []
    a['mrkdwn_in'] = ["pretext", "text", "fields"]

    idea_count = Idea.objects.filter(company=c, deleted=False).count()
    # a['fields'].append({'title':'Ideas', 'value':idea_count, 'short':True})

    comment_count = Comment.objects.filter(idea__company=c).count()
    # a['fields'].append({'title':'Comments', 'value':comment_count, 'short':True})

    member_count = Member.objects.filter(company=c).count()
    # a['fields'].append({'title':'Members', 'value':member_count, 'short':True})

    # a['fields'].append({'title':'Created', 'value':c.created_at.strftime('%Y-%m-%d'), 'short':True})
    a['text'] = "%s ideas • %s comments • %s members • %s activities • Created at %s" % (idea_count, comment_count, member_count, c.activity_count, c.created_at.strftime('%Y-%m-%d'))


    attachments.append(a)

# payload['text'] = 'Company stats for ' + timezone.now().strftime('%Y-%m-%d')
# payload['text'] += '\n__________________________________________'
payload['attachments'] = attachments
requests.post(slack_webhook, json.dumps(payload), headers={'content-type': 'application/json'})


