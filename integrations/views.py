import tweepy
import requests
import json
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site


from users.models import Company

from django.contrib.auth.models import Group, Permission


def get_api():
    API_KEY = "jZapKwEHZsdBdnNAz1bkwuA4G"
    API_SECRET = "bT5m6lPnHWjpfpFFMHo48HHdoePkyOXrSET1vL0zwc2S8wMhBf"
    ACCESS_TOKEN = "4370869513-8HUvpUxaGvzdFaZiHR3WtjLHTGM3I8uuce5a2kF"
    ACCESS_TOKEN_SECRET = "dfHaV6aUu94AuMWUObXPv3nASqyXhAunJqNfGpgSULKiY"

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def has_admin_permission(user, company):
    if company.created_by == user:
        user.user_detail.company = company;
        return 1
    elif user in Group.objects.get(name=company.slug).user_set.all():
        return 1
    return 0


def slack_redirect(request):
    try:
        company = request.user.user_detail.company
        print '######SLACK REDIRECT'
        print company
    except:
        return HttpResponseForbidden()      

    code = request.GET.get('code', None)
    if code:
        if request.is_secure():
            redirect_url = ''.join(['https://', get_current_site(None).domain, '/_slack_redirect/'])
        else:
            redirect_url = ''.join(['http://', get_current_site(None).domain, '/_slack_redirect/'])

        print 'redirect_url: ', redirect_url

        url = "https://slack.com/api/oauth.access?client_id=3943897829.16305580643&client_secret=4a8acb52f59311aa7794a6ed6db090cb&code="+code+'&redirect_uri=' + redirect_url
        resp = requests.get(url)
        data = json.loads(resp.text)
        print data
        if 'ok' in data and data['ok'] == True:
            company.slack = data
            company.save()
        return HttpResponseRedirect( '/' + company.slug + '/settings/#slack-integration' )
    else:
        return HttpResponse('')


def slack(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    if has_admin_permission(request.user, company):
        pass
    else:
        return HttpResponseForbidden()  

    reset = request.GET.get('reset', None)
    if reset:
        company.slack = None
        company.save()
        return HttpResponseRedirect( '/' + company.slug + '/settings/#slack-integration' )

    if request.is_secure():
        redirect_url = ''.join(['https://', get_current_site(None).domain, '/_slack_redirect/'])
    else:
        redirect_url = ''.join(['http://', get_current_site(None).domain, '/_slack_redirect/'])


    return render(request,'integrations/slack.html', {
        'redirect_url': redirect_url,
      })    


def get_tweet(tweet_id):
    api = get_api()
    tweet = api.get_status(tweet_id, trim_user=False, include_entities=False)
    return tweet


@login_required
def search_twitter(request, company_slug):
    api = get_api()

    company = get_object_or_404(Company, slug=company_slug)
    print company.created_by
    print request.user
    if has_admin_permission(request.user, company):
        pass
    else:
        return HttpResponseForbidden()  

    tweets = None
    tweet_count = None
    q = request.GET.get('q', None)
    if q:
        max_tweets = 200
        tweets = [status for status in tweepy.Cursor(api.search, q=q + ' -filter:retweets', include_entities=False, lang="en").items(max_tweets)]


    if tweets is not None:
        tweet_count = len(tweets)

    return render(request,'integrations/twitter_results.html', {
        'company': company,
        'tweets': tweets,
        'tweet_count': tweet_count,
        'q': q,
      })