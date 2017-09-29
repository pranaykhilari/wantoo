import re
import json
import time
import stripe
import logging
import datetime
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, Http404, \
    HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from .models import Company, Member, FeatureCompany, StripeDetails, DarkLaunch, Plan, StripeWebhook
from .forms import NotificationsForm
from idea.models import Activity, Idea, Comment, Vote

from django.contrib.auth.models import Group, Permission

from allauth.account.views import SignupView

from idea.views import has_admin_permission
from django.contrib.auth import authenticate, login

# from django.views.generic.edit import FormView
# from .models import SignupForm


def member_detail(request, company_slug, user_id):
    company = get_object_or_404(Company, slug=company_slug)
    member = get_object_or_404(User, pk=user_id)

    idea_count = Idea.objects.filter(created_by=member, company=company).count()
    want_count = Vote.objects.filter(user=member, idea__company=company).count()
    comment_count = Comment.objects.filter(created_by=member, idea__company=company).count()

    sort = request.GET.get('filter', None)
    activity = Activity.objects.filter(user=member, company=company)
    if sort:
        activity = activity.filter(action=sort)

    return render(request, 'member_detail.html', {
        'company': company,
        'activity': activity[:100],
        'member': member,
        'idea_count': idea_count,
        'want_count': want_count,
        'comment_count': comment_count,
    })


@login_required
def preferences(request):
    # if request.user.id != int(user_id):
    #     return HttpResponseForbidden()

    # company = get_object_or_404(Company, slug=company_slug)
    # member = get_object_or_404(User, pk=user_id)

    if request.method == 'POST' and 'first_name' in request.POST and 'last_name' in request.POST:
        request.user.first_name = request.POST['first_name'].strip()
        request.user.last_name = request.POST['last_name'].strip()
        request.user.save()
        return HttpResponseRedirect('/my-boards/')

    return render(request, 'preferences/profile.html', {
        # 'company':company,
        # 'member':member,
    })


# @login_required
# def subscription(request):
#
#     return render(request,'preferences/subscription.html', {
#
#       })


@login_required
def notification_settings(request):
    # if request.user.id != int(user_id):
    #     return HttpResponseForbidden()

    # company = get_object_or_404(Company, slug=company_slug)
    # member = get_object_or_404(Member, company=company, user__id=user_id)

    if request.method == 'POST':
        notification_settings_form = NotificationsForm(request.POST, instance=request.user.user_detail)
        if notification_settings_form.is_valid():
            notification_settings_form.save()
            return HttpResponseRedirect('/my-boards/')
    else:
        notification_settings_form = NotificationsForm(instance=request.user.user_detail)

    return render(request, 'preferences/notifications.html', {
        # 'company':company,
        # 'member':member,
        'notification_settings': notification_settings_form,
    })


@login_required
def my_boards(request):
    user_boards = Company.objects.filter(created_by=request.user)
    memberships = Member.objects.filter(user=request.user, company__deleted=False).exclude(company__in=user_boards)
    admin_groups = request.user.groups.filter(permissions=Permission.objects.get(codename='is_company_admin'))
    admin_groups = admin_groups.values_list('name', flat=True)

    featured_boards = FeatureCompany.objects.all().order_by('-id')

    check_closed = Company.deleted_objects.filter(created_by=request.user)
    if check_closed.exists():
        check_closed = True
    else:
        check_closed = False

    return render(request, 'my_boards.html', {
        'memberships': memberships,
        'my_boards': user_boards,
        'admin_groups': admin_groups,
        'featured': featured_boards,
        'check_closed': check_closed,
    })


@login_required
def my_closed_boards(request):
    user_boards = Company.deleted_objects.filter(created_by=request.user)

    return render(request, 'my_closed_boards.html', {
        'my_closed_boards': user_boards,
    })


@login_required
def toggle_closed(request, company_slug):
    """Toggles the closed board status of a given board/company. Adds them to the admin group if user is not an admin."""

    company = Company.objects.filter(created_by=request.user, slug=company_slug)
    if company.exists():
        try:
            company = Company.objects.get(created_by=request.user, slug=company_slug)
        except:
            print 'Company not found...'
        company.deleted = True
    else:
        try:
            company = Company.deleted_objects.get(created_by=request.user, slug=company_slug)
        except:
            print 'Company not found...'
        company.deleted = False

    # Board owner is always an admn
    if request.user != company.created_by:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    company.save()
    return HttpResponseRedirect('/my-boards/')


class SignupViewExt(SignupView):
    plan_type = None

    def get_context_data(self, **kwargs):
        context = super(SignupViewExt, self).get_context_data(**kwargs)
        context['plan_type'] = self.plan_type
        return context

        # def get_context_data(self, **kwargs):
        #     context = super(SignupViewExt, self).get_context_data(**kwargs)
        #     context['my_param'] = 'my value'
        #     return context

        # print '##########################SELF PARAM#########################'
        # print self.plan_type
        # template_name = "account/main_signup.html"


# class altSignupView(FormView):
#     template_name = 'account/alt_signup.html'
#     form_class = SignupForm()
#     view_name = 'adwords_landing'
#     success_url = None

# adwords_landing = altSignupView.as_view()


@login_required
def subscription(request):

    try:
        user_stripe_detail = StripeDetails.objects.get(user=request.user)

        if user_stripe_detail.discount_amount:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription_id = stripe.Subscription.retrieve(user_stripe_detail.subscription_id)
            coupon_valid = subscription_id.discount.coupon.valid
            if not coupon_valid:
                user_stripe_detail.discount_amount = None
                user_stripe_detail.save()

        return render(request, 'preferences/subscription.html', {'user_stripe_detail': user_stripe_detail,
                                                                 'plan': user_stripe_detail.plan})
    except StripeDetails.DoesNotExist:
        return render(request, 'preferences/subscription.html')



@login_required
def subscription_payment(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        user_stripe_detail = StripeDetails.objects.get(user=request.user)
        cust = stripe.Customer.retrieve(user_stripe_detail.stripe_customer_id)
        cust_email = cust.email
        source = cust.sources
        cust_data = source.data[0]
        exp_mnth = cust_data.exp_month
        exp_year = cust_data.exp_year
        cust_name = cust_data.name
        last4 = cust_data.last4
        card_no = "**** **** **** " + last4

        user_plan_id = StripeDetails.objects.get(user=request.user).plan_id
        plan_type = Plan.objects.get(id=user_plan_id).plan_type
        plan = Plan.objects.get(id=user_plan_id)
        if plan_type == "starter_monthly":
            plan = Plan.objects.get(plan_type="starter_monthly")
        elif plan_type == "pro_25_monthly":
            plan = Plan.objects.get(plan_type="pro_25_monthly")
        else:
            if request.POST.get("starter"):
                plan = Plan.objects.get(plan_type="starter_monthly_without_trial")
            elif request.POST.get('pro'):
                plan = Plan.objects.get(plan_type="pro_25_monthly_without_trial")
        return render(request, 'preferences/subscription_signin_signup.html', {
            'plan': plan,
            'name': cust_name,
            'email': cust_email,
            'exp_year': exp_year,
            'exp_month': exp_mnth,
            'card_no': card_no,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
    except StripeDetails.DoesNotExist:
        if request.POST.get("starter"):
            plan = Plan.objects.get(plan_type="starter_monthly")
        elif request.POST.get('pro'):
            plan = Plan.objects.get(plan_type="pro_25_monthly")

        email = request.user.email
        return render(request, 'preferences/subscription_signin_signup.html',
                      {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, 'plan': plan, 'email': email})

@login_required
def update_subscription(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        token = request.POST['stripeToken']

        coupon = request.POST['promo']
        stripe_email = request.POST['email']
        plan_type = request.POST['plan_type']
        plan = Plan.objects.get(plan_type=plan_type)
        try:
            user_stripe_detail = StripeDetails.objects.get(user=request.user)
            customer = stripe.Customer.retrieve(user_stripe_detail.stripe_customer_id)
            customer.email = stripe_email
            customer.card = token
            customer.save()
            if user_stripe_detail.subscription_id:
                subscription_response = stripe.Subscription.retrieve(user_stripe_detail.subscription_id)

            if user_stripe_detail.subscription_id is None:
                try:
                    if coupon:
                        subscription_response = stripe.Subscription.create(customer=customer.id, plan=plan.plan_type,
                                                                       coupon=coupon, trial_end="now")
                        plan_amount = subscription_response.plan.amount
                        amount_off = subscription_response.discount.coupon.amount_off
                        percent_off = subscription_response.discount.coupon.percent_off

                        if amount_off:
                            plan_charges = (plan_amount - amount_off) / 100

                        else:
                            convert_plan_amount = plan_amount / 100
                            convert_percent_off = (percent_off * convert_plan_amount) / 100
                            plan_charges = convert_plan_amount - convert_percent_off

                        source = customer.sources
                        cust_data = source.data[0]
                        last4 = cust_data.last4
                        renew_date = datetime.datetime.fromtimestamp(subscription_response.current_period_end)
                        source = customer.sources
                        cust_data = source.data[0]
                        user_stripe_detail.card_last_digits = cust_data.last4
                        user_stripe_detail.stripe_email = customer.email
                        user_stripe_detail.is_cancel = False
                        user_stripe_detail.discount_amount = plan_charges
                        user_stripe_detail.save()

                    else:
                        subscription_response = stripe.Subscription.create(customer=customer.id, plan=plan.plan_type,
                                                                       trial_end="now")
                    if plan.plan_type != "free_monthly" and plan.plan_type != "starter_monthly":
                        for feature in DarkLaunch.objects.all():
                            feature.users.add(request.user)

                    user_stripe_detail.subscription_id = subscription_response.id
                    user_stripe_detail.plan = plan
                    user_stripe_detail.renew_date = datetime.datetime.fromtimestamp(subscription_response.current_period_end)
                except stripe.APIConnectionError:
                    pass
            source = customer.sources
            cust_data = source.data[0]
            user_stripe_detail.card_last_digits = cust_data.last4
            user_stripe_detail.stripe_email = customer.email
            user_stripe_detail.is_cancel = False
            user_stripe_detail.save()

        except StripeDetails.DoesNotExist:
            try:
                customer = stripe.Customer.create(email=stripe_email, card=token)
                if coupon:
                    subscription_response = stripe.Subscription.create(customer=customer.id, plan=plan.plan_type,
                                                                       coupon=coupon)

                    plan_amount = subscription_response.plan.amount
                    amount_off = subscription_response.discount.coupon.amount_off
                    percent_off = subscription_response.discount.coupon.percent_off

                    if amount_off:
                        plan_charges = (plan_amount - amount_off) / 100

                    else:
                        convert_plan_amount = plan_amount / 100
                        convert_percent_off = (percent_off * convert_plan_amount) / 100
                        plan_charges = convert_plan_amount - convert_percent_off

                    source = customer.sources
                    cust_data = source.data[0]
                    last4 = cust_data.last4
                    renew_date = datetime.datetime.fromtimestamp(subscription_response.current_period_end)
                    StripeDetails.objects.create(user=request.user,
                                                 stripe_customer_id=customer.id,
                                                 subscription_id=subscription_response.id,
                                                 plan=plan,
                                                 stripe_email=stripe_email,
                                                 card_last_digits=last4,
                                                 is_cancel=False,
                                                 renew_date=renew_date,
                                                 discount_amount=plan_charges
                                                 )

                else:
                    subscription_response = stripe.Subscription.create(customer=customer.id, plan=plan.plan_type)
                    source = customer.sources
                    cust_data = source.data[0]
                    last4 = cust_data.last4
                    renew_date = datetime.datetime.fromtimestamp(subscription_response.current_period_end)

                    StripeDetails.objects.create(user=request.user,
                                                 stripe_customer_id=customer.id,
                                                 subscription_id=subscription_response.id,
                                                 plan=plan,
                                                 stripe_email=stripe_email,
                                                 card_last_digits=last4,
                                                 is_cancel=False,
                                                 renew_date=renew_date
                                                 )
                if plan.plan_type != "free_monthly" and plan.plan_type != "starter_monthly":
                    for feature in DarkLaunch.objects.all():
                        feature.users.add(request.user)
            except stripe.APIConnectionError:
                logger.exception('Could not connect to stripe')
        except KeyError:
            global logger
            logging.getLogger('stripe_payment called without required POST data')
            return HttpResponseBadRequest('bad POST data')
    return redirect('subscription')



@login_required
def cancel_subscription(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        user_stripe_detail = StripeDetails.objects.get(user=request.user)
        subscription = stripe.Subscription.retrieve(user_stripe_detail.subscription_id)
        subscription.delete(at_period_end=True)

        user_stripe_detail.is_cancel = True
        user_stripe_detail.end_date = datetime.datetime.fromtimestamp(subscription.current_period_end)
        user_stripe_detail.renew_date = None
        user_stripe_detail.modified_at = datetime.datetime.now()
        user_stripe_detail.save()

    except StripeDetails.DoesNotExist:
        logging.getLogger('Cancel subscription exeception')

    return HttpResponseRedirect("/accounts/preferences/subscription/")


def downgrade_subscription(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        user_stripe_detail = StripeDetails.objects.get(user=request.user)
        subscription = stripe.Subscription.retrieve(user_stripe_detail.subscription_id)
        subscription_status = subscription.status
        if subscription_status == "trialing":
            subscription.plan = "starter_monthly"  # Downgrade to pro plan from starter plan
            subscription.save()
            user_stripe_detail.plan_id = Plan.objects.get(plan_type="starter_monthly").pk
            user_stripe_detail.save()
        else:
            subscription.plan = "starter_monthly_without_trial"
            subscription.save()
            user_stripe_detail.plan_id = Plan.objects.get(plan_type="starter_monthly_without_trial").pk
            user_stripe_detail.save()

        for feature in DarkLaunch.objects.all():
            feature.users.remove(request.user)

        user_boards = Company.objects.filter(created_by=request.user, is_private=True)
        for board in user_boards:
            board.deleted = True
            board.save()

    except StripeDetails.DoesNotExist:
        logging.getLogger('Downgrade subscription exception')
    return HttpResponseRedirect("/accounts/preferences/subscription/")

@login_required
def upgrade_to_pro(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user_stripe_detail = StripeDetails.objects.get(user=request.user)
        subscription = stripe.Subscription.retrieve(user_stripe_detail.subscription_id)
        subscription_status = subscription.status
        if subscription_status == "trialing":
            subscription.plan = "pro_25_monthly"  # Upgrade to pro plan from starter plan
            subscription.save()
            user_stripe_detail.plan_id = Plan.objects.get(plan_type="pro_25_monthly").pk
            user_stripe_detail.save()
        else:
            subscription.plan = "pro_25_monthly_without_trial"
            subscription.save()
            user_stripe_detail.plan_id = Plan.objects.get(plan_type="pro_25_monthly_without_trial").pk
            user_stripe_detail.save()

        for feature in DarkLaunch.objects.all():
            feature.users.add(request.user)

    except StripeDetails.DoesNotExist:
        logging.getLogger('Upgrade subscription exception')
    return HttpResponseRedirect("/accounts/preferences/subscription/")


@login_required
def pro_plan(request):
        email = request.user.email
        return render(request, 'account/pro_subscribe.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                                                              'email': request.user.email, 'plan': 'pro_25_monthly'
                                                              })

@login_required
def starter_plan(request):
        email = request.user.email
        return render(request, 'account/starter_subscription.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                                                                    'email': request.user.email, 'plan': 'starter_monthly'
                                                                    })

@login_required
def stripecoupon(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        try:
            coupon_response = stripe.Coupon.retrieve(coupon_code)
            return HttpResponse(
                json.dumps(coupon_response),
                content_type="application/json"
            )
        except (Exception):
            return HttpResponse(
                json.dumps('fail'),
                content_type="application/json"
            )
    else:
        return HttpResponseNotFound('No coupon?')


@require_POST
@csrf_exempt
def stripe_webhook(request):
    # Retrieve the request's body and parse it as JSON
    event_json = json.loads(request.body)
    event_id = event_json["id"]
    event_type = event_json["type"]
    data = event_json["data"]
    object = data["object"]
    customer_id = object["customer"]
    try:
        StripeWebhook.objects.create(event_id=event_id, event_type=event_type, customer_id=customer_id,
                                     event=event_json)
        if event_type == "invoice.payment_succeeded":
            if object["object"] == "subscription":
                sub_id = object["id"]
                renew_date = object["current_period_end"]
                user_stripe_detail = StripeDetails.objects.get(stripe_customer_id=customer_id, subscription_id=sub_id)
                user_stripe_detail.renew_date = datetime.datetime.fromtimestamp(renew_date)
                user_stripe_detail.save()
        elif event_type == "customer.subscription.deleted":
            sub_id = object["id"]
            user_stripe_detail = StripeDetails.objects.get(stripe_customer_id=customer_id, subscription_id=sub_id)
            user_stripe_detail.subscription_id = None
            user_stripe_detail.is_cancel = False
            user_stripe_detail.renew_date = None
            user_stripe_detail.end_date = None
            user_stripe_detail.plan = Plan.objects.get(plan_type="free_monthly")
            user_stripe_detail.save()

            for feature in DarkLaunch.objects.all():
                feature.users.remove(user_stripe_detail.user)

            user_boards = Company.objects.filter(created_by=user_stripe_detail.user, deleted=False)
            if user_boards:
                for board in user_boards:
                    board.deleted = True
                    board.save()

    except:
        pass
    return HttpResponse(status=200)

def private_login_view(request):
    username = request.POST['login']
    password = request.POST['password']
    next = request.POST['next']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(next)

    else:
        messages.add_message(request, messages.ERROR, 'You have entered an invalid password')
        return HttpResponseRedirect(next)


