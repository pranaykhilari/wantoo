import sys, os
import random, string

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(THIS_DIR, ".." ))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wantoo.settings'

import django
django.setup()

from idea.models import Subscription

subs = Subscription.objects.filter(key__isnull=True)
for s in subs:
    print s
    s.key = ''.join( random.sample(string.digits+string.letters.lower()+string.letters.upper(), 20) )
    s.save()