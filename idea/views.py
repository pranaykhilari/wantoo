#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main Django Views

These views compose the majority of the app, and deal with the various subdomains in the idea
process. See users.views for user and account logic.

TODO:
    Break down this file, it is getting large.
    Update company_slug to board_slug for all views.
"""

import re
import json
import requests
import urlparse
import unicodecsv as csv
import datetime
import math
import stripe
from bs4 import BeautifulSoup
from django.conf import settings
from django.core import serializers
from django.http import HttpResponseNotFound

from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, Http404, \
    HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.db.models.functions import Lower
from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.decorators import user_passes_test

from decorators import json_response
from integrations.views import get_tweet
from pusher import Pusher

from .models import Idea, Category, Comment, Vote, Activity, Notification, Subscription, Status, send_idea_merge_email
from .forms import IdeaForm, CommentForm, CategoryForm, StatusForm
from users.models import Company, Member, StripeDetails, Plan, DarkLaunch, MemberInvitation
from users.forms import CompanyForm, CompanyAddForm
from templated_emails.utils import send_templated_email
from django.utils.html import strip_tags

def has_admin_permission(user, company):
    """Checks if user is a the owner, or an admin of the board.

    Admin and owners are considered to be the same in this case.
    This is to get around the multi-board implementation, where each
    user has to have a current board set. If the person owns the board
    but is not the current user, set it as their default.

    Args:
        user: A User instance representing a logged in client.
        company: The company the user is trying to access.

    Returns:
        True if user instance has access, false if does not have access.

    TODO:
        Implement user_passes_test() decorator for blocked routes.
    """

    admin_group = Group.objects.get(name=company.slug).user_set.all();
    if company.created_by == user:
        user.user_detail.company = company;
        user.user_detail.save()
    elif not user in admin_group:
        return 0
    return 1


def is_member(user, company):
    """Check if user is member of a company."""
    return Member.objects.filter(user=user, company=company).exists()


def member_or_add(user, company):
    """Check if user is me  mber of a company. If not adds them to the company"""
    if user.is_authenticated() and not has_admin_permission(user, company) and not is_member(user, company):
        if not Member.objects.filter(user=user).exists():
            Member(user=user, company=company).save()
            comp = company.title
            board_name = comp.replace("'", "")
            board = board_name.replace(" ", "-")
            board = board.lower()
            member = Member.objects.filter(user=user)
            if company.created_by != user and member.count() == 1:

                try:
                    send_templated_email([user.email], "emails/sign_up_member", {
                        'full_name': user.get_full_name(),
                        'company': comp,
                        'email': user.email,
                        'board': board
                    })
                except:
                    print 'Email DID NOT send...'


@login_required
def dashboard(request):
    """Used as default redirect in some sections of codebase"""
    return HttpResponseRedirect('/my-boards/')


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response


@login_required
def create_board(request):
    """Board creation is currently handeled in api.py."""

    board = request.user.user_detail.company
    return render(request, 'create_board.html', {
        'company': board,
    })


@login_required
def company_settings(request, company_slug):
    """Handels the board settings configuration. For owner of Admins only.

    Allows users to edit their settings for a board after initial creation. The settings
    view also contains the slack integration settings. Can be reset, and set. For owner of Admins
    only.

    Args:
        company_slug: the unique identifier for the board being accessed.

    Returns:
        A form with the proper settings inputs if requested. Saves the settings for
        the board being accessed when form is posed.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    # For slack settings option
    reset = request.GET.get('reset', None)
    if reset:
        company.slack = None
        company.save()
        return HttpResponseRedirect('/' + company.slug + '/slack/')
    elif request.is_secure():
        redirect_url = ''.join(['https://', get_current_site(None).domain, '/_slack_redirect/'])
    else:
        redirect_url = ''.join(['http://', get_current_site(None).domain, '/_slack_redirect/'])


    # Settings form
    if request.method == 'POST':
        com_obj = request.POST
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company.is_private = com_obj['is_private_1']
            form.save()
            messages.success(request, 'Company settings are updated.')
            return HttpResponseRedirect('/' + company.slug + '/')
    else:
        form = CompanyForm(instance=company)

    return render(request, 'settings.html', {
        'company': company,
        'form': form,
        'redirect_url': redirect_url,
    })


@login_required
def invite(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    return_emails = ""
    message = ""

    if request.method == 'POST':
        return_emails = []
        emails = []
        if request.POST['members']:
            emails = request.POST['members'].split(",")
        email_text = request.POST['email_text']
        if len(emails) > 0:
            for email in emails:
                email = email.strip()
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    try:
                        mem = MemberInvitation.objects.filter(company_id=company.id, member_email=email)
                        if not mem:
                            mem = MemberInvitation(member_email=email, company_id=company.id)
                            mem.save()
                        send_templated_email([email], "emails/invite_member", {
                            'full_name': request.user.get_full_name(),
                            'company_question': company.question,
                            'company_title': company.title,
                            'company_url': company.slug,
                            'member_email': email,
                            'email_text': email_text
                        })
                    except:
                        return_emails.append(email)
                        print 'Email DID NOT send...'
                        pass
                else:
                    return_emails.append(email)
            return_emails = '\n'.join(return_emails)
            if len(return_emails) > 0:
                message = "The following emails were not sent. Double check they are correct."
            else:

                return HttpResponseRedirect('/' + company.slug + '/manage/members/')
        else:
            message = "Please enter some emails"
            return_emails = ""

    return render(request, 'invite.html', {
        'full_name': request.user.get_full_name(),
        'company': company,
        'emails': return_emails,
        'message': message
    })


@login_required
def stats(request, company_slug):
    """All statistics pertaining to a board instance.

    Args:
        company_slug: the unique identifier for the board being accessed for stats.

    Returns:
        Various charts and visual diagrams for the company stats. Most data is contained in the
        activity graph.

    TODO: Clean up the actual template. It is really messy from before.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

        # Get all members with ideas, votes, comments, and non-active members
    members_with_ideas = Member.objects.filter(company=company, user__user_ideas__isnull=False).distinct()
    members_with_votes = Member.objects.filter(company=company, user__user_votes__isnull=False).distinct()
    members_with_comments = Member.objects.filter(company=company, user__user_comments__isnull=False).distinct()
    members_without_activity = Member.objects.filter(
        company=company,
        user__user_comments__isnull=True,
        user__user_votes__isnull=True,
        user__user_ideas__isnull=True
    ).distinct()

    # Wants ctivity for last 90 days
    since = datetime.datetime.now() - datetime.timedelta(days=90)
    # Postgres specific Date/Time Function
    by_day_select = {"day": """DATE_TRUNC('day', created_at)"""}
    # Get a dictionary of dates with their respective activity counts
    activity_timeline_raw = (Activity.objects.filter(company=company, created_at__gte=since)
                             .extra(select=by_day_select)
                             .values('day')
                             .annotate(num_posts=Count('id'))
                             .order_by('-day'))

    activity_timeline = {}
    for a in activity_timeline_raw:
        activity_timeline[a['day'].date()] = a['num_posts']

    # Fill formatted dictionary with days with no activity
    today = datetime.datetime.today()
    for i in range(90):
        date = (today - datetime.timedelta(days=i)).date()
        if date not in activity_timeline:
            activity_timeline[date] = 0

    # Get list of tuple pairs
    activity_timeline = activity_timeline.items()
    activity_timeline.sort(key=lambda x: x[0])

    # Fetch status Statistics
    statuses = []
    status_list = Status.objects.filter(company=company).order_by('order')
    ideas_without_status = Idea.objects.filter(company=company, status__isnull=True).count()
    no_status_vote_count = Vote.objects.filter(idea__company=company, idea__status__isnull=True).values(
        'user__id').distinct().count()
    statuses.append(
        {'label': 'No status', 'count': ideas_without_status, 'color': 'EEEEEE', 'vote_count': no_status_vote_count})
    for status in status_list:
        idea_count = status.status_ideas.all().count()
        statuses.append(
            {'label': status.title, 'count': idea_count, 'color': status.color, 'vote_count': status.vote_count})

    return render(request, 'stats.html', {
        'company': company,
        'statuses': statuses,
        'members_with_ideas': members_with_ideas,
        'members_with_votes': members_with_votes,
        'members_with_comments': members_with_comments,
        'members_without_activity': members_without_activity,
        'activity_timeline': activity_timeline,
    })


@login_required
def all_activity(request):
    """Fetches list of recent activty accross platform."""

    activity = Activity.objects.all()[:100]
    return render(request, 'activity.html', {
        'company': None,
        'activity': activity,
    })


def activity(request, company_slug):
    """Per board activty streams. Takes a filter query parameter. Lists 30 activities per page.

    Args:
        company_slug: the unique identifier for the board being accessed for stats.

    Returns:
        List of all activity for the board. This is not specific to what the user has doen,
        as is the case with notications.

    TODO: Make a global notifications stream for the my-boards view.
    """

    company = get_object_or_404(Company, slug=company_slug)

    member_exist = allow_board_access(request, company)
    if company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })

    # Apply filter to list if needed. No need for escape()
    sort = request.GET.get('filter', None)
    activity_list = Activity.objects.filter(company=company)
    if sort:
        activity_list = activity_list.filter(action=sort)

    paginator = Paginator(activity_list, 30)
    page = request.GET.get('page')
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)

    return render(request, 'activity.html', {
        'company': company,
        'activity': activities,
    })


@login_required
def notifications(request, company_slug):
    """Fetches all the notifications for a user given a company instance, and displays theem.

    There is a seperate API handel for the notifications tab in the header. This logic is located
    in the api.py file.

    Args:
        company_slug: the unique identifier for the board being accessed for stats.

    Returns:
        A list of all notifications. Note that these notifications are generated when someone interacts with an
        idea the user has previously interacted with. Example, someone comments on an idea the user likes. See
        api.py for more details on this.

    TODO: Clean up the actual template. It is really messy from before.
    """

    company = get_object_or_404(Company, slug=company_slug)

    member_exist = allow_board_access(request, company)
    if company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })

    notifications = Notification.objects.filter(user=request.user, idea__company=company)[:100]

    return render(request, 'notifications.html', {
        'company': company,
        'all_notifications': notifications,
    })


@login_required
@json_response
def clear_notifications(request, company_slug):
    """Clears notifications when the route is accessed.

    Currently being used through AJAX on the front-end. The notifcations are marked as 'seen'
    in the model to stop them from reapprearing in the stream located in the header.
    See the api.js file for more details.

    Args:
        company_slug: the unique identifier for the board related to the notifications.

    Returns:
        JSON response to the client, indicating a success or failure in updating the notification instance.

    TODO: Clean up the actual template. It is really messy from before.
    """

    company = get_object_or_404(Company, slug=company_slug)

    member_exist = allow_board_access(request, company)
    if company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })

    try:
        Notification.objects.filter(user=request.user, idea__company=company, seen=False).update(seen=True)
        return {'success': True, 'message': 'Notifications cleared'}
    except:
        return {'success': False, 'message': 'Failed to clear notifications'}


def mute_subscription(request, sub_key):
    """Unsubscribes user from email updates on a specific idea, as subscriptions are based on a per idea basis.

    Args:
        sub_key: this is sent along with a link to the route that is mapped to this view. Is unique to the subsricption
        instance.

    Returns:
        Plain text repsonse of if their mute status was updated. Failure can come from wrong sub key.

    TODO: Make a template for this response, plain text looks cheap.
    """

    try:
        sub = Subscription.objects.get(key=sub_key)
        sub.muted = True
        sub.save()
        return HttpResponse("Success! You won't receive any emails for this idea. Thank you.")
    except:
        return HttpResponse("Something went wrong. Please contact the Wantoo administrators. Thank you.")


@login_required
def members(request, company_slug):
    """Fetch list of members for a board instance. Seperates and specifies admins for the board.

    Args:
        company_slug: the unique identifier for the board.

    Returns:
        A list of members and admins. Member objects should be checked against admins to determine their status in
        the template

    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    owner = Member.objects.filter(company=company, user=company.created_by)
    members = Member.objects.filter(company=company, ).exclude(user=owner[0].user_id)
    pending_members = MemberInvitation.objects.filter(company_id=company.id)
    try:
        admins = Group.objects.get(name=company.slug).user_set.all()
    except Group.DoesNotExist:
        admins = None

    return render(request, 'members.html', {
        'company': company,
        'pending_members': pending_members,
        'members': members,
        'owner': owner,
        'admins': admins,
    })


@login_required
def export_members(request, company_slug):
    """Exports a downloadable CSV file of all board members.

    Args:
        company_slug: the unique identifier for the board from which members will be printed.

    Returns:
        A CSV file which displays a table as indicated below.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

        # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    filename = company.slug + '_members.csv'
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    writer = csv.writer(response)
    # Table header
    writer.writerow([
        'Member',
        'Email',
        'Ideas',
        'Comments',
        'Votes',
        'Joined at'
    ])
    members = Member.objects.filter(company=company)
    for member in members:
        # Table row, which correspond to the header row above.
        writer.writerow([
            member.user.get_full_name(),
            member.user.email,
            member.idea_count,
            member.comment_count,
            member.vote_count,
            member.created_at.date()
        ])

    return response


@login_required
def toggle_member_block(request, company_slug, member_id):
    """Toggles blocked status for a given member given their id.

    Members of companies can be blocked by the admin of a board. This view is accessed through the
    members list and can be changed by owenrs and admin. If the member is blocked, they become unblocked
    and vice-versa.

    Args:
        company_slug: the unique identifier for the board.
        member_id: the unique identifier for the member the action is being preformed on.

    Returns:
        Returns the original template with applied changes

    """
    company = get_object_or_404(Company, slug=company_slug)
    member = get_object_or_404(Member, pk=member_id, company=company)

    if not has_admin_permission(request.user, member.company):
        return HttpResponseForbidden()

    member.blocked = not member.blocked
    member.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def toggle_admin_status(request, company_slug, member_id):
    """Toggles the admin status of a given user. Adds them to the admin group if user is not an admin.

    Admins are currently implemented as using Django groups. This function adds and removes a specificed
    user from a particular admin group related to the board being accessed.

    Args:
        company_slug: the unique identifier for the board.
        member_id: the unique identifier for the member the action is being preformed on.

    Returns:
        Returns the original template with applied changes
    """

    company = get_object_or_404(Company, slug=company_slug)
    member = get_object_or_404(Member, pk=member_id, company=company)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

        # Board owner is always an admn
    if member.user == company.created_by:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Prevent user from switching their own privilages.
    if member.user == request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Add of remove from the admin group

    group = Group.objects.get(name=company.slug)
    if member.user.groups.filter(name=company.slug).exists():
        member.user.groups.remove(group)
        if not member.user.groups.all().exists():
            for feature in DarkLaunch.objects.all():
                feature.users.remove(member.user)

    else:
        member.user.groups.add(group)
        for feature in DarkLaunch.objects.all():
            feature.users.add(member.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def manage(request, company_slug):
    """Redirect to avoid broken link. Used to point to stats, now points to idea, which is more logical"""
    return HttpResponseRedirect('/' + company_slug + '/stats/')

@login_required
def category_list(request, company_slug):
    """List of all categories for a specific company instance.

    TODO: Pagination once users start adding many categories.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    return render(request, 'category_list.html', {
        'company': company,
    })


@login_required
def status_list(request, company_slug):
    """List of all statuses for a specific company instance. Accessed in the status config view.

    TODO:
        Pagination once users start adding many categories.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    return render(request, 'status_list.html', {
        'company': company,
    })


@login_required
def add_status(request, company_slug):
    """Handels adding a new status type from the status config view.

    When POST, creates new Status instance with the specified options from the
    StatusForm ModelForm.

    Args:
        company_slug: the unique identifier for the board to which the status if being added to..

    Returns:
        Returns the original template with applied changes.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = StatusForm(company, request.POST)
        if form.is_valid():
            status = Status()
            status = form.save(commit=False)
            status.company = company
            status.created_by = request.user
            status.save()
            messages.success(request, 'status added.')
            return HttpResponseRedirect('/' + company.slug + '/manage/statuses/')
    else:
        form = StatusForm(company)

    return render(request, 'status_form.html', {
        'company': company,
        'form': form,
    })


@login_required
def edit_status(request, company_slug, status_id):
    """Handels changing the options of a status instance.

    Allows users to edit their status for a board after initial creation.

    Args:
        company_slug: the unique identifier for the board.
        status_id: the id of the status being edited.

    Returns:
        A form with the proper settings inputs if requested. Saves the settings for
        the board being accessed when form is posed.
    """

    status = get_object_or_404(Status, id=status_id, company__slug=company_slug)
    if not has_admin_permission(request.user, status.company):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = StatusForm(status.company, request.POST, instance=status)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/' + status.company.slug + '/manage/statuses/')
    else:
        form = StatusForm(status.company, instance=status)

    return render(request, 'status_form.html', {
        'status': status,
        'company': request.user.user_detail.company,
        'form': form,
    })


@login_required
@require_POST
def delete_status(request, company_slug):
    """Deletes a status created by the user.

    Currently being accessed through the status edit form. There is a modal who's action
    points to here. Status ID is sumbitted with the form.

    Args:
        company_slug: the unique identifier for the board.

    Returns:
        Redirect to the status list if success.
    """

    status = get_object_or_404(Status, company__slug=company_slug, pk=request.POST['status_id'])
    if not has_admin_permission(request.user, status.company):
        return HttpResponseForbidden()

    status.delete()
    return HttpResponseRedirect('/' + status.company.slug + '/manage/statuses/')


@login_required
def merge_idea(request, company_slug, idea_id):
    """Preforms the idea merge feature, which is a PRO feature. Allows for one idea to be
    merged in to another idea.

    Allows the use to first search for an idea that will consume the slave idea.
    Once selected, form is POSTED and this view habdels this. The idea that is consuming
    the other idea inherits the votes, activities and notificaitons.

    Args:
        company_slug: the unique identifier for the board which the ideas belong to.
        idea_id:  the unique identifier for the idea that is being consumed by the master idea.

    Returns:
        Redirect to the status list if success.
    """

    # The slave idea that will be consumed.
    idea = get_object_or_404(Idea, company__slug=company_slug, pk=idea_id)
    if not has_admin_permission(request.user, idea.company):
        return HttpResponseForbidden()

    if request.method == 'POST' and 'merge_into_id' in request.POST:
        merge_into_idea = get_object_or_404(Idea, pk=request.POST['merge_into_id'], company=idea.company)
        if merge_into_idea.keywords:
            merge_into_idea.keywords = merge_into_idea.keywords + ' ' + idea.title
        else:
            merge_into_idea.keywords = idea.title
        idea.merged_into = merge_into_idea
        idea.save()
        merge_into_idea.save()

        # Move votes
        votes = Vote.objects.filter(idea=idea)
        for vote in votes:
            vote.idea = merge_into_idea
            try:
                vote.save()
            except:
                pass

        # Move activities
        activities = Activity.objects.filter(idea=idea, action='idea_wanted')
        for activity in activities:
            activity.idea = merge_into_idea
            try:
                activity.save()
            except:
                pass

        # Move notifications
        notifications = Notification.objects.filter(idea=idea, action='idea_wanted')
        for notification in notifications:
            notification.idea = merge_into_idea
            try:
                notification.save()
            except:
                pass

                # Send merge notification email
        send_idea_merge_email(idea, merge_into_idea)

        return HttpResponseRedirect('/' + str(idea.id) + '/')

    merge_idea_list = Idea.objects.filter(company=idea.company).filter(merged_into__isnull=True).exclude(
        pk=idea.id).order_by(Lower('title'))

    return render(request, 'merge_idea.html', {
        'company': idea.company,
        'idea': idea,
        'merge_idea_list': merge_idea_list,
    })


def company_home(request, company_slug):
    """The main homepage for a given board.

    If a authenticated user visits this route, they will be automatically added as a member of the board.
    With this comes a welcome email so they know they are now members of the community.

    Args:
        company_slug: the unique identifier for the board.

    Returns:
        Returns the main homepage template, or the redirects if specified.
    """
    try:
        company = get_object_or_404(Company, slug=company_slug)
        member_exist = allow_board_access(request, company)
        override_base = "base.html"
        if company.is_private and (not request.user.is_authenticated or not member_exist):
            override_base = "base_plain.html"
        # Seem to be used by the modals for redirects after actions are preformed.
        redirect_url = request.COOKIES.get("redirect_url", None)
        if redirect_url:
            response = HttpResponseRedirect(redirect_url)
            response.delete_cookie('redirect_url')
            return response

        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })
    except:
        return render(request, 'closed_boards_page.html', {
        })


def company_forum(request, company_slug):
    """The main list of all ideas that belong to a company.

    Note this is currently primarily rendered on the front-end with React (the actual list view).

    Args:
        company_slug: the unique identifier for the board.

    Returns:
        Returns the main base template the embedded information for react to use.
    """

    # Add the user to the community if it is there first time visiting. NOPE THIS IS REMOVED NOW....
    company = get_object_or_404(Company, slug=company_slug)
    member_exist = allow_board_access(request, company)
    if company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })
    # if (request.user.is_authenticated()
    #     and not has_admin_permission(request.user, company)
    #     and not is_member(request.user, company)):
    #         Member(user=request.user, company=company).save()

    # Seem to be used by the modals for redirects after actions are preformed.
    redirect_url = request.COOKIES.get("redirect_url", None)
    if redirect_url:
        response = HttpResponseRedirect(redirect_url)
        response.delete_cookie('redirect_url')
        return response

    # Get the list of ideas
    ideas = Idea.objects.filter(company=company)
    status = request.GET.get('status', None)
    if status:
        status = Status.objects.get(company=company, pk=status)
        ideas = ideas.filter(status=status)
    else:
        ideas = ideas.exclude(status__closed=True)

    # Don't show merged ideas
    ideas = ideas.filter(merged_into__isnull=True)

    # remove tabs...
    for idea in ideas:
        idea.title = idea.title.replace('\n', '<br />').replace('\r', '<br />').replace('\t', '<br />')

    display_count = ideas.count()
    sort = request.GET.get('sort', None)
    if sort == 'new':
        ideas = ideas.order_by('-id')
    elif sort == "random":
        ideas = ideas.order_by('?')
    else:
        ideas = ideas.order_by('-vote_count')

    paginator = Paginator(ideas, 50)  # Show 50 ideas per page
    page = request.GET.get('page')
    try:
        idea_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        idea_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        idea_list = paginator.page(paginator.num_pages)

    # print '##############json form list###################'
    # idea_list_json = serializers.serialize('json', [idea_list,])
    # print idea_list_json



    return render(request, 'forum.html', {
        'company': company,
        'ideas': idea_list,
        'display_count': display_count,
        'status': status,
    })


def category_ideas(request, company_slug, category_id):
    """Same as the main company list view, but filters the list per catgory.

    Args:
        company_slug: the unique identifier for the board.
        category_id: the category id used to filter the list.

    Returns:
        Returns the main base template with the list inforation for React.
    """

    category = get_object_or_404(Category, pk=category_id, company__slug=company_slug)

    member_exist = allow_board_access(request, category.company)
    if category.company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': category.company,
            'member_exist': member_exist,
            'override_base': override_base
        })

    ideas = Idea.objects.filter(category=category)

    status = request.GET.get('status', None)
    if status:
        status = Status.objects.get(company=category.company, pk=status)
        ideas = ideas.filter(status=status)
    else:
        ideas = ideas.exclude(status__closed=True)

    # Don't show merged ideas
    ideas = ideas.filter(merged_into__isnull=True)
    display_count = ideas.count()

    sort = request.GET.get('sort', None)
    if sort == 'new':
        ideas = ideas.order_by('-id')
    elif sort == "random":
        ideas = ideas.order_by('?')
    else:
        ideas = ideas.order_by('-vote_count')

    return render(request, 'forum.html', {
        'category': category,
        'company': category.company,
        'ideas': ideas,
        'display_count': display_count,
        'status': status,
    })


def idea_redirect(request, idea_id):
    """Used to redirect to idea detail view from a short url."""
    idea = get_object_or_404(Idea, pk=idea_id)
    return HttpResponseRedirect(idea.get_absolute_url())


def idea_detail(request, company_slug, idea_id, idea_slug):
    """ The idea details page with commenting and supporter information

    Idea slug is used for SEO purposed I suspect. It is not actually used by
    the logic.

    Args:
        company_slug: the unique identifier for the board.
        idea_id: the idea id corresponding to the idea being displayed.

    Returns:
        Returns the idea detail infromation.
    """
    idea = get_object_or_404(Idea, pk=idea_id, company__slug=company_slug)
    company = get_object_or_404(Company, slug=company_slug)

    member_exist = allow_board_access(request, company)
    if company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })

    recent_ideas = Idea.objects.filter(company__slug=company_slug, merged_into__isnull=True).order_by('-id')[:3]
    merged_ideas = Idea.objects.filter(company__slug=company_slug, merged_into=idea.id).order_by('-id')

    return render(request, 'idea_detail.html', {
        'idea': idea,
        'recent_ideas': recent_ideas,
        'merged_ideas': merged_ideas,
        'company': company,
        'comments': idea.idea_comments.all().order_by('created_at'),
    })


@login_required
def idea_list(request, company_slug):
    """Lists ideas for board owner or admin to manage from manage view."""

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    category_id = request.GET.get('category', None)
    ideas = Idea.objects.filter(company=company)
    if category_id:
        ideas = ideas.filter(category__pk=category_id)

    return render(request, 'idea_list.html', {
        'company': company,
        'admin_ideas': ideas,
    })


@login_required
def add_category(request, company_slug):
    """Adds a new category using a ModalForm.

    Once information is sent using POST, new catgeroy instance is created
    and associated with the board instance specified.

    Args:
        company_slug: the unique identifier for the board.

    Returns:
        Returns the Modal form. If POST, creates the instance.
    """
    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CategoryForm(company, request.POST)
        if form.is_valid():
            cat = Category()
            cat = form.save(commit=False)
            cat.company = company
            cat.created_by = request.user
            cat.save()
            messages.success(request, 'Category added.')
            return HttpResponseRedirect('/' + company.slug + '/manage/categories/')
    else:
        form = CategoryForm(company)

    return render(request, 'category_form.html', {
        'company': company,
        'form': form,
    })


@login_required
def edit_category(request, company_slug, category_id):
    """Handels changing the options of a category instance.

    Allows users to edit their category for a board after initial creation.

    Args:
        company_slug: the unique identifier for the board.
        category_id: the id of the category being edited.

    Returns:
        A form with the proper settings inputs if requested. Saves the settings for
        the board being accessed when form is posed.
    """

    category = get_object_or_404(Category, id=category_id, company__slug=company_slug)
    if not has_admin_permission(request.user, category.company):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CategoryForm(category.company, request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return HttpResponseRedirect('/' + category.company.slug + '/manage/categories/')
    else:
        form = CategoryForm(category.company, instance=category)

    return render(request, 'category_form.html', {
        'category': category,
        'company': category.company,
        'form': form,
    })


@login_required
@require_POST
def delete_category(request, company_slug):
    """Deletes a status created by the user."""

    category = get_object_or_404(Category, company__slug=company_slug, pk=request.POST['category_id'])
    if not has_admin_permission(request.user, category.company):
        return HttpResponseForbidden()

    category.delete()
    messages.info(request, 'Category deleted.')
    return HttpResponseRedirect('/' + category.company.slug + '/manage/categories/')


@login_required
def add_idea(request, company_slug):
    """Adds an idea from a ModelForm which is sent along with original request.

    This is used primarily for the twitter integration now. Usually an admin will only use
    this view for adding a manual idea. If a tweet_id is found, the tweet is diaplayed along
    with the regular template. When Posted, the tweet information is stored along with the new
    instance of the idea.

    Args:
        company_slug: the unique identifier for the board the idea is being added to.

    Returns:
        The modealForm used with the optional embedded tweet.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    try:
        member = Member.objects.get(company=company, user=request.user)
        if member.blocked:
            return HttpResponseForbidden()
    except:
        pass

    tweet_id = request.GET.get('tweet', None)
    if not tweet_id:
        if request.method == 'POST' and 'tweet_id' in request.POST:
            tweet_id = request.POST['tweet_id']

    tweet = {}
    tweet_text = ''
    if tweet_id:
        tweet_result = get_tweet(tweet_id)
        tweet['id'] = tweet_id
        tweet['text'] = tweet_result.text
        tweet_text = tweet_result.text
        tweet['created_at'] = tweet_result.created_at
        tweet['name'] = tweet_result.author.name
        tweet['screen_name'] = tweet_result.author.screen_name

    if request.method == 'POST':
        form = IdeaForm(company, request.POST)
        if form.is_valid():
            idea = Idea()
            idea = form.save(commit=False)
            idea.title = request.POST['title'].strip()
            idea.company = company
            idea.created_by = request.user
            if tweet:
                idea.tweet = tweet
            idea.save()

            if request.user.user_detail.company != company:
                idea.new = True
                idea.save()
            messages.success(request, 'Idea added.')
            if idea.tweet:
                return HttpResponseRedirect(
                    '/' + company.slug + '/twitter/?idea=' + str(idea.id) + '&tweet=' + str(tweet_id));
            return HttpResponseRedirect('/' + company.slug + '/ideas/?sort=new')
    else:
        form = IdeaForm(company, initial={'description': tweet_text})

    return render(request, 'add_idea.html', {
        'company': company,
        'form': form,
        'tweet': tweet,
    })


@csrf_exempt
@require_POST
@json_response
def _delete_ideas(request, company_slug):
    """End point for deleting ideas.

    TODO:
        Move these to the api.py file. There was a FIXIT note left for this before
        by the last dev
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    post_data = json.loads(request.body)
    if not 'ideas' in post_data:
        return {'success': False, 'message': 'Ideas missing.'}

    for idea_id in post_data['ideas']:
        try:
            idea = Idea.objects.get(company__slug=company_slug, pk=idea_id)
            idea.deleted = True
            idea.save()
            # Delete all related activities
            activities = Activity.objects.filter(idea=idea)
            activities.delete()
        except:
            # FIXIT: log this
            pass
    messages.info(request, 'Ideas deleted.')
    return {'success': True, 'message': 'Ideas deleted.'}


@csrf_exempt
@require_POST
@json_response
def _move_ideas(request, company_slug):
    """End point for moving ideas.

    TODO:
        Move these to the api.py file. There was a FIXIT note left for this before
        by the last dev
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    post_data = json.loads(request.body)
    if not 'ideas' in post_data or not 'category' in post_data:
        return {'success': False, 'message': 'Required parameters missing.'}

    try:
        category = Category.objects.get(company=company, pk=post_data['category'])
    except:
        return {'success': False, 'message': 'Category does not exists.'}

    for idea_id in post_data['ideas']:
        try:
            idea = Idea.objects.get(company__slug=company_slug, pk=idea_id)
            idea.category = category
            idea.save()
        except:
            # FIXIT: log this
            pass
    messages.info(request, 'Ideas moved to the selected category.')
    return {'success': True, 'message': 'Ideas moved.'}


@login_required
def edit_idea(request, company_slug, idea_id):
    """Handels changing the options of a idea instance.
    Allows users to edit any idea after it has been added. In these
    cases, the board admin or owner would be able to change the status,
    category, title, etc of the idea. If the member is blocked they
    should not get access to this page...
    Args:
        company_slug: the unique identifier for the board.
        idea_id: the id of the idea being changed.
    Returns:
        A form with the proper settings inputs if requested. Saves the settings for
        the board being accessed when form is posed.
    """

    idea = get_object_or_404(Idea, company__slug=company_slug, pk=idea_id)
    if not has_admin_permission(request.user, idea.company) and idea.created_by != request.user:
        return HttpResponseForbidden()

    try:
        member = Member.objects.get(company=idea.company, user=request.user)
        if member.blocked:
            return HttpResponseForbidden()
    except:
        pass

    if request.method == 'POST':
        print 'Idea Before EDIT'
        print idea.__dict__
        form = IdeaForm(idea.company, request.POST, instance=idea)

        status = idea.status

        if form.is_valid():
            idea = form.save(commit=False)

            if (not request.POST.get('status', False)
                and not has_admin_permission(request.user, idea.company)):
                idea.status = status
            idea.title = strip_tags(idea.title).encode('utf8')
            idea.edited_by = request.user
            if idea.title:
                idea.save()
            messages.success(request, 'Idea updated.')
            print 'Idea After EDIT'
            print idea.__dict__
            return HttpResponseRedirect(idea.get_absolute_url())
    else:
        form = IdeaForm(idea.company, instance=idea)

    return render(request, 'add_idea.html', {
        'idea': idea,
        'company': idea.company,
        'form': form,
    })



@login_required
@require_POST
def delete_idea(request, company_slug):
    """Deletes an idea created by the user.

    NOTE, that currently the system is keeping deleted idea in the
    database, and simily indicating it is deleted through an attribute. This is
    for flexability in the future, inorder to restore, archive, etc. Endpoint
    being used as an AJAX endpoint for deleting ideas.

    Args:
        company_slug: the unique identifier for the board.

    Returns:
        Redirect to the  homepage or the manage section.

    TODO:
        Maybe clean the system of deleted ideas. Not wanted for now
    """

    idea = get_object_or_404(Idea, company__slug=company_slug, pk=request.POST['idea_id'])
    if has_admin_permission(request.user, idea.company) or idea.created_by == request.user:
        pass
    else:
        return HttpResponseForbidden()

    idea.deleted = True
    idea.save()
    messages.info(request, 'Idea deleted.')
    if idea.created_by == request.user:
        return HttpResponseRedirect('/' + idea.company.slug + '/')
    else:
        return HttpResponseRedirect('/' + idea.company.slug + '/manage/ideas/')


@login_required
def reset_new_idea_status(request):
    """The new image tag used be for someof the admin views.

    TODO: Move this to a CSS file.
    """
    ideas = Idea.objects.filter(company=request.user.user_detail.company, new=True)
    for idea in ideas:
        idea.new = False
        idea.save()
    pixel = """
    R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
    """.strip().decode('base64')
    return HttpResponse(pixel, content_type='image/gif')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# The following three functions where from an old search feature TODO: Delete these soon.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


@csrf_exempt
def search(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    query_string = ''
    found_entries = None
    ideas = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'description', ])

        ideas = Idea.objects.filter(company=company).filter(entry_query).order_by('-created_at')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'search_results.html',
                  {'query_string': query_string, 'ideas': ideas, 'company': company, })


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#





@login_required
@csrf_exempt
def export_ideas(request, company_slug):
    """Exports a downloadable CSV file of all board ideas.

    Args:
        company_slug: the unique identifier for the board from which ideas will be printed.

    Returns:
        A CSV file which displays a table as indicated below.
    """

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

        # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    filename = company.slug + '_' + str(datetime.datetime.now().date()) + '.csv'
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    writer = csv.writer(response)
    writer.writerow(['Idea', 'Category', 'Status', 'Vote count', 'Author', 'Author email', 'Added at'])

    ideas = Idea.objects.filter(company=company)
    for idea in ideas:
        writer.writerow([idea.title, idea.category, idea.status, idea.vote_count, idea.created_by.get_full_name(),
                         idea.created_by.email, idea.created_at.date()])
    return response


@login_required
@csrf_exempt
def import_ideas(request, company_slug):
    """Imports ideas from a textbox and adds them to the database."""

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    failed_ideas = []

    if request.method == 'POST':
        if request.POST['category']:
            category = get_object_or_404(Category, company=company, pk=request.POST['category'])
        else:
            category = None
        ideas = request.POST['ideas'].splitlines()

        for idea in ideas:
            if len(idea) >= 1 and len(idea) <= 70:
                try:
                    Idea.objects.get(category=category, company=company, title=idea.strip())
                    failed_ideas.append(idea.title)
                    continue
                except:
                    Idea(title=idea.strip(), created_by=request.user, category=category, company=company,
                         imported=True).save()
            else:
                failed_ideas.append(idea.title)

    return render(request, 'import_ideas.html', {
        'company': company,
        'failed_ideas': failed_ideas
    })


@login_required
@csrf_exempt
def import_uv(request, company_slug):
    """Imports ideas from a Uservoice link. Need to look this over more if will be used..."""

    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    if not request.is_ajax() or not request.POST['uv_url']:
        return render(request, 'import_uv.html', {
            'company': company,
        })

    START_URL = request.POST['uv_url'].strip()
    try:
        BASE = START_URL.split('forums/')[0]
    except:
        return HttpResponse(json.dumps({'success': False, 'message': 'Invalid link.'}), "application/json")

    def abs_url(soup):
        return urlparse.urljoin(BASE, soup['href'])

    def get_soup(url):
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        return soup

    def get_ideas(soup):
        ideas = []
        for idea in soup.findAll("li", {"class": "uvIdea"}):
            title = idea.find("h2", {"class": "uvIdeaTitle"})
            desc = idea.find("div", {"class": "uvIdeaDescription"})
            title = title.text.strip()

            print(title)
            print '-----'
            # print(desc.text.strip())
            ideas.append({'idea': title})
        pusher = Pusher(app_id=u'150241', key=u'8d396c4a64f32d61c897', secret=u'e9751c3da92985c13900')
        pusher.trigger(company.slug, 'idea_imported', ideas)

        current_page = soup.find("div", {"class": "uvPagination"}).find("em", {"class": "current"})
        try:
            print ("Current page number: " + current_page.text)
            next_link = soup.find("div", {"class": "uvPagination"}).find("a", {"rel": "next"})
            next_link = abs_url(next_link)
            print ('NEXT: ' + next_link)
            get_ideas(get_soup(next_link))
        except:
            pass

    soup = get_soup(START_URL)
    get_ideas(soup)
    return HttpResponse(json.dumps({'success': True, 'message': 'Imported.'}), "application/json")


@login_required
def kanban(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()

    ideas = Idea.objects.filter(company=company, merged_into=None).order_by('order')

    # fix for linebreak bug in base.html template
    length = ideas.count() + 1
    for idea in ideas:
        idea.description = idea.description.replace('\n', '<br />').replace('\r', '<br />')
        idea.title = idea.title.replace('\n', '<br />').replace('\r', '<br />')
        if math.isnan(idea.order):
            idea.order = length
            length = length + 1

    return render(request, 'kanban/kanban.html', {
        'company': company,
        'ideas': ideas,
    })


@login_required
def resend_email(request):
    if request.method == 'GET':
        company_slug = request.GET.get('company')
        email = request.GET.get('email')
        company = get_object_or_404(Company, slug=company_slug)
        email = email.strip()

        try:
            send_templated_email([email], "emails/invite_member", {
                'full_name': request.user.get_full_name(),
                'company_question': company.question,
                'company_title': company.title,
                'company_url': company.slug,
                'member_email': email
            })
        except:
            print 'Sorry unable to send mail now'
    return HttpResponseNotFound('temporary unavailable')

def board_access(request):
    if request.method == 'GET':
        email_value = request.GET.get('email_value')
        comp = request.GET.get('company')
        company = get_object_or_404(Company, slug=comp)
        invited_mem = MemberInvitation.objects.filter(company_id=company.id, member_email=email_value)
        user1 = None
        member_exist = None
        if company.is_private:
            try:
                user1 = User.objects.get(email=email_value).pk
                if user1:
                    member_exist = Member.objects.filter(company=company, user=user1)
                else:
                    member_exist = False
            except:
                member_exist = False

            if invited_mem and not user1:
                return HttpResponse(
                    json.dumps('signup'),
                    content_type="application/json"
                )
            if invited_mem or member_exist:
                return HttpResponse(
                    json.dumps('true'),
                    content_type="application/json"
                )
            if invited_mem and user1:
                return HttpResponse(
                    json.dumps('true'),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps('false'),
                    content_type="application/json"
                )

    return HttpResponseNotFound('Email value unavailable')

def allow_board_access(request, company):
    if company.is_private:
        try:
            if request.user.is_authenticated:
                member_exist = is_member(request.user, company)
                pending_invitations = MemberInvitation.objects.filter(company_id=company.id,
                                                                      member_email=request.user.email)
                member = Member()
                if member_exist:
                    return True
                elif pending_invitations:
                    member.user = request.user
                    member.company = company
                    member.save()
                    pending_invitations.delete()
                    return True
                else:
                    return False
        except:
            return False
    else:
        return True

@login_required()
def remove_invitee(request, company_slug, member_id):
    company = get_object_or_404(Company, slug=company_slug)
    pending_invitee = get_object_or_404(MemberInvitation, pk=member_id, company_id=company.id)
    pending_invitee.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))