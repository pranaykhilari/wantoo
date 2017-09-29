from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.http import HttpResponseRedirect

def home(request):
    if request.user.is_authenticated():
      return HttpResponseRedirect('/my-boards/')
    return render(request,'landing/homev3.html')

def team(request):
    return render(request,'landing/team.html', {
      })

def careers(request):
    return render(request,'landing/careers.html', {
      })

def privacy(request):
    return render(request,'landing/privacy.html', {
      })

def terms_use(request):
    return render(request,'landing/terms-of-use.html', {
      })

def terms_service(request):
    return render(request,'landing/terms-of-service.html', {
      })

def signup(request, plan_type_from_url):
    plan_type = 'error'

    if request.user.is_authenticated():
      return HttpResponseRedirect('/my-boards/')

    #TODO: Add plan_type list check
    if plan_type_from_url:
        plan_type = plan_type_from_url

    return render(request,'account/main_signup.html', {
        'plan_type': plan_type
      })


def alt_signup(request, ad_group_from_url, ad_type_from_url):
    plan_type = 'error'

    if request.user.is_authenticated():
      return HttpResponseRedirect('/my-boards/')

    #TODO: Add plan_type list check
    if ad_type_from_url:
        ad_type = ad_type_from_url

    if ad_group_from_url:
        ad_group = ad_group_from_url

    return render(request,'account/alt_signup.html', {
        'ad_type': ad_type,
        'ad_group': ad_group,
       })