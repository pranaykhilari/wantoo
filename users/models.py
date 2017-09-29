from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django import forms
from django.core.exceptions import ValidationError
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from collections import OrderedDict
from jsonfield import JSONField
from utils import SlugifyUnicode, SlugifyUniquely

from templated_emails.utils import send_templated_email


class NonDeleted(models.Manager):
    """Django Manager interface to deligate queries to deletable objects.

    Used by the Ideas and Comments models in order to avoid querying deleting
    objects. Currently these objects are kept in the database, to have the ability
    to resotore the ideas before. 
    """

    def get_queryset(self):
        """Returns the filtered query set containing only active ideas."""
        print 'NonDeleted(models.Manager) called...'
        return super(NonDeleted, self).get_queryset().filter(deleted=False)


class Deleted(models.Manager):
    """Django Manager interface to deligate queries to deletable objects.

    Used by closed boards view to get all closed boards
    """

    def get_queryset(self):
        """Returns the filtered query set containing only active ideas."""
        print 'Deleted(models.Manager) called...'
        return super(Deleted, self).get_queryset().filter(deleted=True)


class Company(models.Model):
    title = models.CharField('Company name', max_length=55)
    logo_url = models.URLField(default="http://wantoo.io/static/dashboard/img/company_logos/sample-logo.jpg", null=True, blank=True)
    color = models.CharField(default="3284FF", max_length=7, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    slack = JSONField(null=True, blank=True)
    blank_home = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_company')
    question = models.CharField(default="We'd love your feedback. Tell us what you want.", max_length=200, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    # _default_manager = NonDeleted()

    #this base manager sometimes creates blank objects in some queries. Watch out for this
    # _base_manager = NonDeleted()

    objects = NonDeleted()
    deleted_objects = Deleted()

    def save(self):
        if not self.id:
            slug = SlugifyUnicode(self.title, '-')
            reserved_slugs = [  'admin', 'accounts', 'company', 'stuff', 'settings', 'idea', 
                                'ideas', 'api', 'team', 'careers', 'privacy', 'manage']
            if slug in reserved_slugs:
                slug = slug + '-board'      
            self.slug = SlugifyUniquely(slug, Company)
        super(Company, self).save()

    @property
    def idea_count(self):        
        from idea.models import Idea
        return Idea.objects.filter(company=self).exclude(merged_into__isnull=False).count()

    @property
    def active_idea_count(self):        
        from idea.models import Idea
        return Idea.objects.filter(company=self).exclude(merged_into__isnull=False).exclude(status__closed=Truestatus__closed).count()

    @property
    def new_idea_count(self):        
        from idea.models import Idea
        return Idea.objects.filter(company=self, new=True).count()

    @property
    def comment_count(self):        
        from idea.models import Comment
        return Comment.objects.filter(idea__company=self).count()

    @property
    def vote_count(self):        
        from idea.models import Vote
        return Vote.objects.filter(idea__company=self).count()

    @property
    def activity_count(self):        
        from idea.models import Activity
        return Activity.objects.filter(company=self).count()

    @property
    def member_count(self):        
        return Member.objects.filter(company=self).count()

    def __unicode__(self):
        return self.title

    def non_deleted(self):
        if self.deleted:
            return False
        return True

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Companies"
        # default_manager_name = "NonDeleted"


class UserDetail(models.Model):
    user = models.OneToOneField(User, related_name='user_detail')
    phone =  models.CharField(max_length=12, null=True, blank=True)
    company = models.ForeignKey(Company, related_name='user_company', null=True, blank=True)
    casl = models.BooleanField(default=False)

    email_comment = models.BooleanField(default=True)
    email_want = models.BooleanField(default=False)
    email_comment_on_want = models.BooleanField(default=True)
    email_comment_on_comment = models.BooleanField(default=True)
    email_digest = models.BooleanField(default=True)

    @property
    def board_count(self):
        try: 
            return Company.objects.filter(created_by=self.user).count()
        except:
            return 0

    def __unicode__(self):
        return '%s' % self.user.username

    class Meta:
        unique_together = ('user', 'company')
        verbose_name = "User Detail"


class DarkLaunch(models.Model):
    feature_tag = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='user_features', blank=True)
    created_by = models.ForeignKey(User, related_name='user_created_features')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.feature_tag

    class Meta:
        verbose_name = "Dark Launch Code"
        verbose_name_plural = "Dark Launch Codes"


class FeatureCompany(models.Model):
    title = models.CharField(max_length=55, null=True, blank=True)
    question = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    company = models.ForeignKey(Company, related_name='featured_companies')
    created_by = models.ForeignKey(User, related_name='user_featured_companies')

    class Meta:
        verbose_name = "Featured Board"
        verbose_name_plural = "Featured Boards"


class Member(models.Model):
    company = models.ForeignKey(Company, related_name='company_members')
    user = models.ForeignKey(User, related_name='member_companies')
    blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def idea_count(self):        
        from idea.models import Idea
        return Idea.objects.filter(company=self.company, created_by=self.user).count()

    @property
    def comment_count(self):        
        from idea.models import Comment
        return Comment.objects.filter(idea__company=self.company, created_by=self.user).count()

    @property
    def vote_count(self):        
        from idea.models import Vote
        return Vote.objects.filter(idea__company=self.company, user=self.user).count()                

    def __unicode__(self):
        return '%s @ %s' %(self.user.username, self.company.title)

    class Meta:
        unique_together = ('user', 'company')
        verbose_name = "User Membership"


class SignupForm(forms.Form):
    full_name = forms.CharField(max_length=50, label='Full name')
    casl = forms.ChoiceField(   widget=forms.CheckboxInput, 
                                required=False, 
                                choices=[(True, 'Yes'), (False, 'No')],
                                label="It's okay to send me email about the wantoo service"
                                )
    # company_name = forms.CharField(max_length=255, required=True)
    # first_name = forms.CharField(max_length=30, label='First name')
    # last_name = forms.CharField(max_length=30, label='Last name')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full name'
        # No need for password repeat
        # del(self.fields['password2'])
        # self.fields['first_name'].widget.attrs['placeholder'] = 'First name' 
        # self.fields['last_name'].widget.attrs['placeholder'] = 'Last name' 

        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['email'].widget.attrs['maxlength'] = "150"

        if 'autofocus' in self.fields['username'].widget.attrs:
            del self.fields['username'].widget.attrs['autofocus'] 
        if 'password1' in self.fields:
            fields_key_order = ['full_name', 'email', 'username', 'password1', 'password2', 'casl']
            self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)


    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].split()
        if len(full_name[0]) < 1 or len(' '.join(full_name[1:])) < 1:
            raise ValidationError("Please provide a first and last name.")
        return self.cleaned_data['full_name'].strip() 


    # def clean_email(self):
    #     username = self.cleaned_data['email']
    #     if len(username) > 30:
    #         raise ValidationError("Please use a shorter email address.")
    #     return username


    def save(self, user):
        name_list = self.cleaned_data['full_name'].split()
        user.first_name = name_list[0]
        user.last_name = ' '.join(name_list[1:])
        user.username = self.cleaned_data['email']
        user.save()
        # company = Company()
        # company.title = self.cleaned_data['company_name']
        # company.created_by = user
        # company.save()

        user_detail = UserDetail()
        user_detail.user = user
        # user_detail.company = company
        if 'casl' in self.cleaned_data:
            user_detail.casl = True
        else:
            user_detail.casl = False
        user_detail.save()

           
@receiver(user_signed_up)
def create_user_detail(sender, **kwargs):
    user = kwargs.pop('user')
    request = kwargs.pop('request')
    plan_type = request.POST.get('plan_type', False)
    # if plan_type  == 'pro':
    #     for feature in DarkLaunch.objects.all():
    #             feature.users.add(user)

    ######### 
    usr_name = user.get_full_name()
    usr_email =  user.email
    if not plan_type:
        plan_type = 'NO PLAN TYPE'
    try:
        send_templated_email(['help@wantoo.io'], "emails/sign_up_admin", {
            'full_name': usr_name,
            'author_email': usr_email,
            'plan_type': plan_type,
        })
    except:
        print 'Email didnt end...'
    #########   

    try:
        user_detail = UserDetail.objects.get(user=user)
        return
    except:
        user_detail = UserDetail()
        user_detail.user = user
        if 'casl' in request.POST:
            user_detail.casl = True
        else:
            user_detail.casl = False
        user_detail.save()


@receiver(post_save, sender=Company)
def company_created(sender, instance, created, **kwargs):
    print 'company statueses'
    if created:
        from idea.models import Status
        Status(company=instance, title='Not planned', order=0, color="b5b5b5", created_by=instance.created_by, closed=True).save()
        Status(company=instance, title='Planned', order=3000, color="3eaae5", created_by=instance.created_by).save()
        Status(company=instance, title='Completed', order=6000, color="66961a", created_by=instance.created_by, closed=True).save()
        Member(company=instance, user=instance.created_by).save()



@receiver(user_signed_up)
def set_mixpanel_profile(sender, **kwargs):
    request = kwargs.pop('request')
    request.session['set_mixpanel_profile'] = True


class Plan(models.Model):
    name = models.CharField(max_length=32)
    plan_type = models.CharField(max_length=32)
    interval = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=32)
    description = models.CharField(max_length=20, blank=True, null=True)
    trial_period_days = models.IntegerField()


class StripeDetails(models.Model):
    user = models.ForeignKey(User, max_length=16, related_name='user_id')
    stripe_customer_id = models.CharField(max_length=32, blank=True, null=True)
    subscription_id = models.CharField(max_length=32, blank=True, null=True)
    plan = models.ForeignKey(Plan, max_length=16, related_name='user_plan_id')
    stripe_email = models.EmailField(default='')
    card_last_digits =  models.CharField(max_length=4, blank=True, null=True)
    is_cancel = models.BooleanField(default=False)
    discount_amount = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    renew_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


class StripeWebhook(models.Model):
    event_id = models.CharField(max_length=32, blank=False, null=False)
    event_type = models.CharField(max_length=32, blank=True, null=True)
    customer_id = models.CharField(max_length=32, blank=True, null=True)
    event = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MemberInvitation(models.Model):
    company_id = models.IntegerField()
    member_email = models.EmailField(default='')