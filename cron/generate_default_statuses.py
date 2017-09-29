import sys, os

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(THIS_DIR, ".." ))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wantoo.settings'

import django
django.setup()

from users.models import Company
from idea.models import Status

companies = Company.objects.filter(company_statuses__isnull=True)
print str(companies.count()) + ' companies with no statuses'
for company in companies:
    Status(company=company, title='Planned', order=5, color="3eaae5", created_by=company.created_by).save()
    Status(company=company, title='Not planned', order=10, color="b5b5b5", created_by=company.created_by, closed=True).save()
    Status(company=company, title='Completed', order=15, color="66961a", created_by=company.created_by, closed=True).save()
