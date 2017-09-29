import unicodecsv as csv

from django.contrib.admin.views.decorators import staff_member_required
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from datetime import datetime, timedelta
from idea.models import Idea, Category, Comment, Vote, Activity, Notification, Subscription, Status
from users.models import Company, Member, DarkLaunch, FeatureCompany

from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

from django.contrib.sites.models import Site

from forms import  AddFeatureBoardForm

@staff_member_required
def home_user(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request,'staff/home_user.html', {
        'users': users,                              
    })


@staff_member_required
def home_user_export(request):

    response = HttpResponse(content_type='text/csv')
    filename = 'staff_users.csv'
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Boards', 'Last Login', 'Joined at'])

    users = User.objects.all().order_by('last_name')

    for user in users:
        try: 
            board_count = user.user_detail.board_count 
        except:
            board_count = 0
        writer.writerow([user.get_full_name(), user.email, board_count, user.last_login, user.date_joined])
    return response

@staff_member_required
def home_board(request):
    companies = Company.objects.all().order_by('-created_at')
    return render(request,'staff/home_board.html', {
        'companies': companies,                              
    })

@staff_member_required
def home_board_export(request):

    response = HttpResponse(content_type='text/csv')
    filename = 'staff_boards.csv'
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    writer = csv.writer(response)
    writer.writerow(['Board Name', 'Ideas', 'Members', 'Owener', 'Created on'])

    companies = Company.objects.all().order_by('title')
    for company in companies:
        writer.writerow([company.title, company.idea_count, company.member_count, company.created_by.get_full_name(), company.created_at])
    return response

@staff_member_required
def featured_boards(request):
    companies = FeatureCompany.objects.all().order_by('-id')

    if request.method == 'POST':
        form = AddFeatureBoardForm(request.POST)
        if form.is_valid():
            company = FeatureCompany()
            company = form.save(commit=False)
            company.created_by = request.user 
            company.save()
            return HttpResponseRedirect( '/staff/featured/#currently-featured' )

    else: 
        form = AddFeatureBoardForm()

    return render(request,'staff/featured_boards.html', {
        'companies': companies,    
        'form': form,      
    })

@staff_member_required
def featured_boards_delete(request, feature_id):

    featued_board = FeatureCompany.objects.filter(id=feature_id)

    if featued_board.exists():
        featued_board.delete()
        return HttpResponseRedirect('/staff/featured/#currently-featured')
    else:
        return HttpResponse("Something went wrong :(")


@staff_member_required
def user_detail(request, user_id):

    user = User.objects.get(id=user_id)
    user_boards = Company.objects.filter(created_by=user)
    memberships = Member.objects.filter(user=user).exclude(company__in=user_boards)
    admin_groups = request.user.groups.filter(permissions=Permission.objects.get(codename='is_company_admin'))
    admin_groups = admin_groups.values_list('name', flat=True)
    current_site = Site.objects.get_current()

    if request.method == 'POST':
        for feature in DarkLaunch.objects.all():
            if feature.users.filter(id=user.id).exists():
                feature.users.remove(user)
            else:
                feature.users.add(user)

    return render(request,'staff/user_detail.html', {
        'user': user,      
        'memberships': memberships,
        'user_boards': user_boards,
        'admin_groups': admin_groups,   
        'domain': current_site.domain                  
    })

@staff_member_required
def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    members_with_ideas = Member.objects.filter(company=company, user__user_ideas__isnull=False).distinct()
    members_with_votes = Member.objects.filter(company=company, user__user_votes__isnull=False).distinct()
    members_with_comments = Member.objects.filter(company=company, user__user_comments__isnull=False).distinct()
    members_without_activity = Member.objects.filter(company=company, user__user_comments__isnull=True, user__user_votes__isnull=True, user__user_ideas__isnull=True).distinct()

    since = datetime.now()-timedelta(days=90)
    by_day_select = {"day": """DATE_TRUNC('day', created_at)"""} # Postgres specific
    activity_timeline_raw = Activity.objects.filter(company=company, created_at__gte=since).extra(select=by_day_select).values('day').annotate(num_posts=Count('id')).order_by('-day')

    activity_timeline = {}
    for a in activity_timeline_raw:
        activity_timeline[a['day'].date()] = a['num_posts']

    today = datetime.today()
    for i in range(90):
        date = ( today-timedelta(days=i) ).date()
        if date not in activity_timeline:
            activity_timeline[date] = 0

    activity_timeline = activity_timeline.items()
    activity_timeline.sort(key=lambda x: x[0])

    return render(request,'staff/company_detail.html', {
        'company': company,                              
        'members_with_ideas': members_with_ideas,
        'members_with_votes': members_with_votes,
        'members_with_comments': members_with_comments,
        'members_without_activity': members_without_activity,
        'activity_timeline': activity_timeline,
    })


@staff_member_required
def company_ideas(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    ideas = Idea.objects.filter(company=company).order_by('-vote_count')

    return render(request,'staff/ideas.html', {
        'company': company,                              
        'ideas': ideas,                              
    })


@staff_member_required
def company_activities(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    activity = Activity.objects.filter(company=company).order_by('-created_at')[:100]

    return render(request,'staff/activities.html', {
        'company': company,                              
        'activity': activity,                              
    })


@staff_member_required
def company_members(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    members = Member.objects.filter(company=company).order_by('-created_at')

    return render(request,'staff/members.html', {
        'company': company,                              
        'members': members,                              
    })


