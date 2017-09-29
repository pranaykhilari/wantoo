from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from users.models import Company, Member

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        referer = request.META.get('HTTP_REFERER')

        # My apologies for this disgusting hack
        company = None
        try:
            company_slug = referer.split('//')[1].split('/')[1]
            company = Company.objects.get(slug=company_slug)
        except:
            pass

        if company:
            # check membership
            try:
                Member.objects.get(company=company, user=request.user)
            except:
                Member(company=company, user=request.user).save()
        return referer
