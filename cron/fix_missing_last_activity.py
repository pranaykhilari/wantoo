import sys, os
import random, string

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(THIS_DIR, ".." ))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wantoo.settings'

import django
django.setup()

from idea.models import Idea, Activity

ideas = Idea.objects.filter(last_activity__isnull=True)
print ideas.count()
print '--'
for idea in ideas:
    print idea.id
    activity = Activity(company=idea.company, idea=idea, user=idea.company.created_by, action='idea_submitted')
    activity.save()
    idea.last_activity = activity
    idea.save()

