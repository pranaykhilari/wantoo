import sys, os, json
from algoliasearch import algoliasearch


THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(THIS_DIR, ".." ))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wantoo.settings'

import django
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F

django.setup()

from idea.models import Idea

# client = algoliasearch.Client("IQKHNBSCI3", "8218775bb7600359f71d7c0de4d1c194")
client = algoliasearch.Client("BZLMDWU1HE", "ac847a22f98dc5c61829d1399a6799f3")


index = client.init_index('Ideas')

ideas = Idea.objects.all().annotate(objectID=F('id')).values('objectID', 'title', 'description', 'category__title', 'company__slug')
# MyModel.objects.annotate(renamed_value=F('cryptic_value_name')).values('renamed_value')

ideas_json = json.dumps(list(ideas), cls=DjangoJSONEncoder)

# print ideas
for idea in ideas:
    print idea
    print ''
index.save_objects(ideas)


