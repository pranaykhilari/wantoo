import datetime, re
from django import template
import random
import hashlib
import hmac
from django.utils.translation import ugettext, ungettext
from django.utils import timezone
from django.utils.safestring import mark_safe
from dateutil import tz, parser as date_parser
from django.conf import settings
from utils import get_gravatar_url

from idea.models import Vote, Notification
from users.models import Member, Company, DarkLaunch, StripeDetails

from django.contrib.auth.models import Group, Permission

#TODO: Use serializers?
from django.core import serializers

register = template.Library()


@register.filter    
def subtract(value, arg):
    return value - arg


@register.simple_tag
def active(request, pattern, second=None, third=None):
    pattern = str(pattern)
    # second = str(second)
    # third = str(third)
    if second:
        pattern += second
    if third:
        pattern += third
    if re.search(pattern, request.get_full_path()):
        return 'active'
    return ''


# get settings value
@register.simple_tag
def get_settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag(takes_context=True)
def small_logo(context):
    try:
        company_slug = context['company'].slug
        if not context['request'].path.endswith(company_slug+'/'):
            return 'comp-header--isLogoSmall'
    except:
        return 'comp-header--isLogoSmall'
    

@register.assignment_tag(takes_context=True)
def get_admin_status(context):
    try:
        company = context['company']
        admin_group = Group.objects.get(name=company.slug).user_set.all()
        user = context['request'].user
    except:
        return False

    if (company.created_by != user
        and user not in admin_group ):
        return False

    return True

@register.assignment_tag(takes_context=True)
def get_user_plan_type(context):
    try:
        user = context['request'].user
        user_stripe_detail = StripeDetails.objects.get(user=user)
        return user_stripe_detail.plan.plan_type
    except:
        return "free_monthly"

@register.assignment_tag(takes_context=True)
def get_dark_launch(context, feature_tag):
    try:
        company = context['company']
        user = context['request'].user
    except:
        return False

    try:
        DarkLaunch.objects.get(feature_tag=feature_tag, users=user)
        return True
    except:
        return False


@register.assignment_tag(takes_context=True)
def get_dark_launch_all(context, user_id):
    
    for feature in DarkLaunch.objects.all():
        if not feature.users.filter(id=user_id).exists():
            return False
    return True


@register.filter(takes_context=True)
def hashtag(source, company):
    
    # find hashtags
    pattern = re.compile(r"(?P<start>.?)#(?P<hashtag>[A-Za-z0-9_]+)(?P<end>.?)")

    # replace with link to search
    link = r'\g<start><a href="/'+ company.slug +'/search/?q=%23\g<hashtag>"  title="#\g<hashtag> search">#\g<hashtag></a>\g<end>'
    text = pattern.sub(link,source)
    return mark_safe(text)


@register.assignment_tag(takes_context=True)
def get_company(context):

    # print '#################################'
    # company_data = serializers.serialize('json', [context['request'].user.user_detail.company,])
    # idea_data = serializers.serialize('json', [context['request'].user.user_detail.company,])
    # print data

    try: 
        return context['request'].user.user_detail.company
    except:
        pass

    try:
        company_slug = context['request'].GET['next'].replace('/', '')
        return Company.objects.get(slug=company_slug)
    except:
        pass

    try:
        company_slug = context['redirect_field_value'].replace('/', '')
        return Company.objects.get(slug=company_slug)
    except:
        pass

    return None


@register.assignment_tag(takes_context=True)
def get_user_hash(context):
    try:
        user = context['request'].user
        user_hash1 = hmac.new(settings.INTERCOM_SECRET_KEY, user.email, digestmod=hashlib.sha256).hexdigest()
        return user_hash1
    except:
        print('No user found')


@register.assignment_tag(takes_context=True)
def get_blocked_status(context):
    try: 
        member = Member.objects.get(company=context['company'], user=context['request'].user)
        return member.blocked
    except:
        return False


@register.assignment_tag(takes_context=True)
def get_notifications(context):
    user = context['request'].user
    return Notification.objects.filter(user=user, idea__company=context['company'])[:10]


@register.assignment_tag(takes_context=True)
def get_has_new_notifications(context):
    user = context['request'].user
    return Notification.objects.filter(user=user, idea__company=context['company'], seen=False).exists()


@register.simple_tag
def vote_status(user, idea):
    try:
        Vote.objects.get(user=user, idea=idea)
        return 'voted'
    except:
        return 'not_voted'


@register.assignment_tag(takes_context=True)
def get_voted_ideas(context):
    try: 
        user = context['request'].user
    except:
        return []
    try:
        company = context['company']
    except:
        return []
    
    votes = Vote.objects.values_list('idea__id', flat=True).filter(idea__company=company, user=user)        
    return list(votes)


@register.simple_tag
def random_int(a,b):
    return random.randint(a,b)


@register.simple_tag(takes_context=True)
def clear_temp_mixpanel_profile(context):
    try:
        del context['request'].session['set_mixpanel_profile']
    except:
        pass
    return ''


@register.simple_tag
def gravatar_url(user, size=80):
    try:
        url = user.socialaccount_set.all()[0].get_avatar_url()
    except:
        url = None

    if url:
        return url
    else:
        return get_gravatar_url(user, size)
        

@register.filter    
def better_timesince(date):  # TODO: let user specify format strings
    """
    Returns a translated, humanized representation of the time delta between
    a given date and the current date.
    Originally from: http://djangosnippets.org/snippets/2275/
    """
    # convert string to date if needed
    if not date:
        date = timezone.now()

    if isinstance(date, (str, unicode)):
        date = date_parser.parse(date)
        # if the date has no timezone, assume UTC
        if date.tzinfo is None:
            date = date.replace(tzinfo=tz.tzutc())

    delta = timezone.now() - date

    num_years = delta.days / 365
    if (num_years > 0):
        return ungettext(u"%d year ago", u"%d years ago", num_years) % (
            num_years,)

    num_months = delta.days / 30
    if (num_months > 0):
        return ungettext(u"%d month ago", u"%d months ago",
            num_months) % num_months

    num_weeks = delta.days / 7
    if (num_weeks > 0):  # TODO: "last week" if num_weeks == 1
        return ungettext(u"%d week ago", u"%d weeks ago",
            num_weeks) % num_weeks

    if (delta.days > 0):  # TODO: "yesterday" if days == 1
        return ungettext(u"%d day ago", u"%d days ago",
            delta.days) % delta.days

    num_hours = delta.seconds / 3600
    if (num_hours > 0):  # TODO: "an hour ago" if num_hours == 1
        return ungettext(u"%d hour ago", u"%d hours ago",
            num_hours) % num_hours

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):  # TODO: "a minute ago" if num_minutes == 1
        return ungettext(u"%d minute ago", u"%d minutes ago",
            num_minutes) % num_minutes

    return ugettext(u"just now")