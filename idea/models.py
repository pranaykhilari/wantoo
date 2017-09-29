"""Main Object Models

This module contains the major models, inclding Category, Idea, 
Status, Vote, Comment, Activity, Subscription and Notifications.

Most of the object attributes are pretty self describing, but they
are documented for ease of use.
"""

import random
import string
import hashlib
import requests
import json

from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.dateformat import format
from django.core.validators import MaxLengthValidator
from django.contrib.sites.shortcuts import get_current_site

from pusher import Pusher
from templated_emails.utils import send_templated_email
from jsonfield import JSONField
from utils import SlugifyUnicode, SlugifyUniquely
from utils import get_gravatar_url

from users.models import Company, Member



class NonDeleted(models.Manager):
    """Django Manager interface to deligate queries to deletable objects.

    Used by the Ideas and Comments models in order to avoid querying deleting
    objects. Currently these objects are kept in the database, to have the ability
    to resotore the ideas before. 
    """

    def get_queryset(self):
        """Returns the filtered query set containing only active ideas."""
        return super(NonDeleted, self).get_queryset().filter(deleted=False)


class Category(models.Model):
    """Idea category model to group ideas by keywords

    Categories belong to a board/company instance, not to the user. Primary use
    is to make sure users and admins can understand which ideas are similar.

    Attributes:
        title: the display name of the category.
        company: the company instance this category was created for.
        created_at: the data the object was created.
        created_by: the user instance the created the object.
    """

    title = models.CharField('Category title', max_length=50)
    company = models.ForeignKey(Company, related_name='company_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_categories')

    @property
    def idea_count(self):        
        ideas = Idea.objects.filter(category=self).count()
        return ideas

    @property
    def active_idea_count(self):        
        ideas = Idea.objects.filter(category=self).exclude(status__closed=True).count()
        return ideas

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"


class Idea(models.Model):
    """A core data structure which holds the ideas users post to Idea Boards
    
    One of the bigger objects used to handle all variations of idea submission,
    which is currently limited to switter and regular from submission. Most activity
    in the system relies on this object. 

    *** -> indicates depreciation or the attribute not being used.

    Attributes:
        title: the main text of the idea. This is what users submit through the form.
        slug: a unique slug that is formed from the idea title on during creation. Main
            role is SEO as it is added to the url when interacting with the idea.
        description: addititional details about the idea that users can add. This is only
            visible in a limited amount of views.
        ***score: seems to be depreciated. Probably used before for inital search.
        status: a status object assigned to the idea. Can be from the default or user created.
        category: the category the idea is grouped in.
        company: this should be board, but refrences the board the idea was added to.
        ***assigned_to: seems to be depreciated.
        created_by: the user instance that submitted the idea to the board.
        created_at: timestamp, currently not used.
        ***edited_at: not being used, but keep as it could be used for admins.
        ***edited_by: not being used, but keep as it could be used for admins.
        merged_into: when idea is merged, idea is kept in store but points to the idea through
            this attriubte.
        ***last_activity: this was previously used to display the last user activity in the
            idea list view. This was then replaced by a new design. Not really being used too
            much.
        vote_count: quick access field for the total votes/supporters for an idea.
        comment_count: quice access field for total comment count for idea.
        ***keywords: seems to be used for Algolia Search. Not displayed on any views currently.
        tweet: if the source of the idea is twitter, this stores the information on the tweet.
        ***published: currently not being used...
        imported: indicates if the ideas were imported through the import feature.
        ***ip: currently not being used...
        ***email: currently not being used...
        new: adds a small badge to the idea for admins when the idea was recently added.
        deleted: indicates that the idea should not be accessable to public. The reason the
            idea stays in the system is for a pissbile future archive feature. The delete_idea
            view has this same logic.
        objects: overrides queries with NonDeleted class

    TO DO:
        Handle all the ideas with ***. These are not being used and should be removed. 
    """

    title = models.TextField(validators=[MaxLengthValidator(70)])
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField('Description', blank=True, validators=[MaxLengthValidator(5000)])
    score = models.IntegerField(default=0)
    status = models.ForeignKey('Status', default=None, related_name='status_ideas', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name='category_ideas', null=True, blank=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, related_name='company_ideas')
    assigned_to = models.ForeignKey(User, related_name='assigned_ideas', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='user_ideas', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, related_name='edited_ideas', null=True, blank=True)
    merged_into = models.ForeignKey('self', blank=True, null=True)
    last_activity = models.ForeignKey('Activity', related_name='activity_idea', null=True, blank=True, on_delete=models.SET_NULL)
    vote_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    keywords = models.TextField(blank=True, null=True)
    tweet = JSONField(blank=True, null=True)    
    published = models.BooleanField(default=False)
    imported = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    new = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    objects = NonDeleted()
    order = models.FloatField(default=0)
    # order = models.DecimalField(max_digits=None, decimal_places=None)

    @property
    def last_activity_action(self):        
        try:
            return self.last_activity.action
        except:
            return None

    @property
    def last_activity_user_id(self):        
        try:
            return self.last_activity.user.id      
        except:
            return None

    @property
    def last_activity_user(self):        
        try:
            return self.last_activity.user.first_name 
        except:
            return None

    @property
    def last_activity_date(self):        
        try:
            return format(self.last_activity.created_at, 'U')
        except:
            return None

    @property
    def last_activity_avatar(self):        
        try:
            return get_gravatar_url(self.last_activity.user)
        except:
            return None                                        

    @property
    def status_color(self):
        if self.status:     
            return self.status.color   
        else:
            return None

#    @property
    def created_by_id(self):        
        try:
            return self.created_by.id
        except:
            return None

#    @property
    def created_by_avatar(self):        
        try:
            return get_gravatar_url(self.created_by)
        except:
            return None

#    @property
    def voted_users_id(self):        
        try:
            return voted_user.user.id
        except:
            return None

    @classmethod
    def get_max_idea_order(cls, company):
        try:
            max_agg_order = cls.objects.filter(company=company).aggregate(Max('order'))
            return max_agg_order['order__max'] + 6000
        except:
            return 6000

    #This function was here before, and seems to be running atleast 3 times when
    #an idea is saved. In order to calc new kanban order once, I am checking the pk
    #value to avoid the muliple calls...
    #http://stackoverflow.com/questions/4269605/django-override-save-for-model
    def save(self, *args, **kwargs):
        self.slug = slugify(' '.join(self.title.split()[:7]))
        
        if self.pk is None:
            self.order = Idea.get_max_idea_order(self.company)    
        try:
            super(Idea, self).save(*args, **kwargs)
            print ' => super(Idea, self).save(*args, **kwargs).save() ran successfully!'
        except Exception as e:
            print ' => super(Idea, self).save(*args, **kwargs).save() failed... '
            print '%s (%s)' % (e.message, type(e))
            pass

    def get_absolute_url(self):
        return reverse('idea_detail', kwargs={'company_slug': self.company.slug, 'idea_id': self.id, 'idea_slug': self.slug})

    def __unicode__(self):
        return self.title

    def non_deleted(self):
        if self.deleted:
            return False
        if self.merged_into:
            return False
        return True            

    class Meta:
        ordering = ['-created_at']


class Status(models.Model):
    title = models.CharField(max_length=20)    
    company = models.ForeignKey(Company, related_name='company_statuses')
    color = models.CharField(max_length=7, default='666666')
    closed = models.BooleanField(default=False)
    order = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_statuses')

    @property
    def count(self):        
        idea_count = Idea.objects.filter(status=self).count()
        return idea_count

    @property
    def vote_count(self):
        return Vote.objects.filter(idea__status=self, idea__company=self.company, idea__deleted=False).count()

    @classmethod
    def get_max_status_order(cls, company):
        max_agg_order = cls.objects.filter(company=company).aggregate(Max('order'))
        return max_agg_order['order__max'] + 3000

    def save(self):
        if self.pk is None:
            try:
                self.order = Status.get_max_status_order(self.company) 
            except:
                pass
        try:
            super(Status, self).save()
            print 'Status Saved.'
        except:
            print 'Something went wrong saving Status.'
            pass

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ('company', 'title')
        ordering = ['order']


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='user_votes')
    idea = models.ForeignKey(Idea, related_name='idea_votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'idea')
        ordering = ['-created_at']


class Comment(models.Model):
    idea = models.ForeignKey(Idea, related_name='idea_comments')
    comment = models.TextField()
    created_by = models.ForeignKey(User, related_name='user_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    flagged = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    objects = NonDeleted()   

    def __unicode__(self):
        return self.comment

    class Meta:
        ordering = ['-created_at']


ACTION_CHOICES = (
    ('idea_submitted','Idea submitted'),
    ('comment_added','Comment added'),
    ('idea_wanted','Idea wanted'),
    ('joined_community','Joined community')
) 


class Activity(models.Model):
    company = models.ForeignKey(Company, related_name='company_activity')
    idea = models.ForeignKey(Idea, related_name='idea_activity', blank=True, null=True)
    comment = models.ForeignKey(Comment, related_name='comment_activity', blank=True, null=True)
    status = models.ForeignKey(Status, related_name='status_activity', blank=True, null=True)
    user = models.ForeignKey(User, related_name='user_activity', blank=True, null=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        out = self.user.get_full_name()
        if self.action == 'idea_submitted':
            out += ' added idea'
        elif self.action == 'comment_added':
            out += ' commented'
        elif self.action == 'idea_wanted':
            out += ' wanted it'
        else:
            return self.action + ' > ' + self.idea.title
        return out 

    class Meta:
        ordering = ['-created_at']


def default_sub_key():
    return ''.join( random.sample(string.digits+string.letters.lower()+string.letters.upper(), 20) )


class Subscription(models.Model):
    idea = models.ForeignKey(Idea, related_name='idea_subscriptions')
    user = models.ForeignKey(User, related_name='user_subscriptions')
    muted = models.BooleanField(default=False)
    key = models.CharField(max_length=20, default=default_sub_key, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.idea) or u''

    class Meta:
        unique_together = ('user', 'idea')
        ordering = ['-created_at']


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='user_notifications')
    created_by = models.ForeignKey(User, related_name='created_notifications')
    idea = models.ForeignKey(Idea, related_name='idea_notifications', blank=True, null=True)
    comment = models.ForeignKey(Comment, related_name='comment_notifications', blank=True, null=True)
    status = models.ForeignKey(Status, related_name='status_notifications', blank=True, null=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    seen = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        out = self.created_by.get_full_name()
        if self.action == 'idea_submitted':
            out += ' added idea'
        elif self.action == 'comment_added':
            out += ' commented'
        elif self.action == 'idea_wanted':
            out += ' wanted it'
        else:
            return self.action + ' > ' + self.idea.title
        return out 

    @property
    def timesince(self):        
        from idea.templatetags import mytags 
        return mytags.better_timesince(self.created_at)

    @property
    def own_idea(self):        
        try:
            return self.idea.created_by == user
        except:
            return False

    @property
    def avatar(self):        
        try:
            return get_gravatar_url(self.created_by)
        except:
            return None     

    class Meta:
        ordering = ['-created_at']


'''
    Activity and notification generators
'''

def create_notification(created_by, idea, action, comment=None):
    if action == "comment_added":
        # get all the subscribers
        subscribers = Subscription.objects.filter(idea=idea).exclude(user=created_by)
        for s in subscribers:
            Notification( user=s.user,
                          created_by=created_by,
                          action=action,
                          idea=idea,
                          comment=comment
                        ).save()

    elif action == "idea_wanted" and idea.created_by != created_by:
        Notification( user=idea.created_by,
                      created_by=created_by,
                      action=action,
                      idea=idea
                    ).save()  

    elif action == "idea_submitted" and idea.created_by != idea.company.created_by:
        Notification( user=idea.company.created_by,
                      created_by=created_by,
                      action=action,
                      idea=idea
                    ).save()   

    elif action == "status_changed":
        # get all the subscribers
        subscribers = Subscription.objects.filter(idea=idea).exclude(user=created_by)
        for s in subscribers:
            Notification( user=s.user,
                          created_by=created_by,
                          action=action,
                          status=idea.status,
                          idea=idea,
                        ).save()



def update_last_idea_activity(idea):
    activity = Activity.objects.filter(idea=idea).latest('id')
    idea.last_activity = activity
    idea.save()    


def update_comment_count(idea):
    idea.comment_count = Comment.objects.filter(idea=idea).count()
    idea.save()  


def update_vote_count(idea):
    idea.vote_count = Vote.objects.filter(idea=idea).count()
    idea.save()

    
def push_event(idea, event, obj):
    pusher = Pusher(app_id=u'150241', key=u'8d396c4a64f32d61c897', secret=u'e9751c3da92985c13900')
    pusher.trigger('idea_'+str(idea.id), event, obj)
 

def notify_admin_for_new_idea(idea):
    idea_url = ''.join(['https://', get_current_site(None).domain, idea.get_absolute_url()])
    edit_url = ''.join(['https://', get_current_site(None).domain, '/' + idea.company.slug + '/edit-idea/' + str(idea.id) + '/'])
    author_url = ''.join(['https://', get_current_site(None).domain, '/' + idea.company.slug + '/member/' + str(idea.created_by.id) +'/' ])

    try:
        send_templated_email([idea.company.created_by.email], "emails/idea_submitted", {
            'idea':idea,
            'first_name':idea.company.created_by.first_name,
            'author_url': author_url,
            'idea_url': idea_url,
            'edit_url': edit_url,
        })                   
    except:
        print 'notify_admin_for_new_idea fail'
        pass    


def send_comment_emails(comment):

    subscribers = Subscription.objects.filter(idea=comment.idea, muted=False).exclude(user=comment.created_by)
    idea_url = ''.join(['https://', get_current_site(None).domain, comment.idea.get_absolute_url()])
    author_url = ''.join(['https://', get_current_site(None).domain, '/' + comment.idea.company.slug + '/member/' + str(comment.created_by.id) +'/' ])

    for s in subscribers:
        membership = Member.objects.get(user=s.user, company=comment.idea.company)

        #muted idea in email
        if s.muted:
            continue

        #created the idea, and doesn't want emails when comments added
        if  s.user == s.idea.created_by and not s.user.user_detail.email_comment:
            continue

        #commented an idea, and doesn't want emails when comments added
        comments = Comment.objects.filter(idea=comment.idea, created_by=s.user).exists()
        print comments
        if comments and not s.user.user_detail.email_comment_on_comment:
            continue

        #wanted idea, and doesn't want emails when comments added
        votes = Vote.objects.filter(idea=comment.idea, user=s.user).exists()
        print 'votes exists'
        if not (s.user == s.idea.created_by) and votes and (not s.user.user_detail.email_comment_on_want):
            continue


        mute_url = ''.join(['https://', get_current_site(None).domain, '/mute/' + s.key + '/'])
        settings_url = ''.join(['https://', get_current_site(None).domain,'/' + comment.idea.company.slug + '/member/' + str(s.user.id) +'/preferences/notifications/' ])
    
        try:
            send_templated_email([s.user.email], "emails/comment_added", {
                'comment':comment,
                'comment_title': unicode(comment.idea.title),
                'first_name':s.user.first_name,
                'idea_url': idea_url,
                'author_url': author_url,
                'user_email': s.user.email,
                'mute_url': mute_url,
                'settings_url': settings_url,
            }, s.idea.company.title + ' <noreply+' + s.idea.company.slug + '@wantoo.io>')       
        except:
            print 'send_comment_emails fail'
            pass            

def send_status_change_email(idea):
    subscribers = Subscription.objects.filter(idea=idea, muted=False).exclude(user=idea.created_by)
    idea_url = ''.join(['https://', get_current_site(None).domain, idea.get_absolute_url()])

    for s in subscribers:
        membership = Member.objects.get(user=s.user, company=idea.company)
        if s.muted:
            continue

        mute_url = ''.join(['https://', get_current_site(None).domain, '/mute/' + s.key + '/'])

        try:
            send_templated_email([s.user.email], "emails/status_changed", {
                'first_name':s.user.first_name,
                'idea_url': idea_url,
                'user_email': s.user.email,
                'mute_url': mute_url,
                'idea': idea,
            }, s.idea.company.title + ' <noreply+' + s.idea.company.slug + '@wantoo.io>')  
        except:
            print 'send_status_change_email fail'
            pass


def send_idea_merge_email(idea, winning_idea):
    subscribers = Subscription.objects.filter(idea=idea, muted=False)
    idea_url = ''.join(['https://', get_current_site(None).domain, idea.get_absolute_url()])
    winning_idea_url = ''.join(['https://', get_current_site(None).domain, winning_idea.get_absolute_url()])

    for s in subscribers:
        membership = Member.objects.get(user=s.user, company=idea.company)
        if s.user == idea.created_by and s.user.user_detail.company == idea.company:
            continue
        if s.muted:
            continue

        mute_url = ''.join(['https://', get_current_site(None).domain, '/mute/' + s.key + '/'])

        try:
            send_templated_email([s.user.email], "emails/idea_merged", {
                'first_name':s.user.first_name,
                'idea_url': idea_url,
                'user_email': s.user.email,
                'mute_url': mute_url,
                'idea': idea,
                'winning_idea': winning_idea,
                'winning_idea_url': winning_idea_url,
            }, s.idea.company.title + ' <noreply+' + s.idea.company.slug + '@wantoo.io>')  
        except:
            print 'send_idea_merge_email fail'
            pass


# Should only be sent to admin
def send_want_email(vote):
    try:
        s = Subscription.objects.get(idea=vote.idea, user=vote.idea.created_by)    
        membership = Member.objects.get(user=vote.idea.created_by, company=vote.idea.company)
    except:
        return False
    if s.muted or not s.user.user_detail.email_want:
        return False

    if vote.user == vote.idea.created_by:
        return False

    idea_url = ''.join(['https://', get_current_site(None).domain, vote.idea.get_absolute_url()])
    author_url = ''.join(['https://', get_current_site(None).domain, '/' + vote.idea.company.slug + '/member/' + str(vote.user.id) +'/' ])

    mute_url = ''.join(['https://', get_current_site(None).domain, '/mute/' + s.key + '/'])

    try:
        send_templated_email([s.user.email], "emails/idea_wanted", {
            'vote':vote,
            'first_name':s.user.first_name,
            'idea_url': idea_url,
            'author_url': author_url,
            'user_email': s.user.email,
            'mute_url': mute_url,
            'settings_url': author_url + 'preferences/notifications/',
        }, s.idea.company.title + ' <noreply+' + s.idea.company.slug + '@wantoo.io>')       
    except:
        print 'send_want_email fail'
        pass


'''
    Signals
'''


@receiver(post_save, sender=Comment)
def comment_added(sender, instance, **kwargs):

    # Check membership
    try:
        member = Member.objects.get(user=instance.created_by, company=instance.idea.company)
    except:
        Member(user=instance.created_by, company=instance.idea.company).save()

    # Create activity
    Activity(company=instance.idea.company, idea=instance.idea, user=instance.created_by, comment=instance, action='comment_added').save()
    update_last_idea_activity(instance.idea)
    update_comment_count(instance.idea)

    # Subscribe to this idea
    subscription, created = Subscription.objects.get_or_create(idea=instance.idea, user=instance.created_by)

    # Create notifications
    create_notification(instance.created_by, instance.idea, 'comment_added', instance)

    # Send push notification 
    new_comment = {}
    new_comment['author'] = instance.created_by.get_full_name()
    new_comment['author_id'] = str(instance.created_by.id)
    new_comment['comment'] = instance.comment
    # MD5 email
    new_comment['email'] = hashlib.md5(instance.created_by.email).hexdigest()
    push_event(instance.idea, 'new_comment', new_comment)

    # Shoot emails
    send_comment_emails(instance)


@receiver(post_delete, sender=Comment)
def comment_deleted(sender, instance, **kwargs):
    # Delete all activities for the comment
    Activity.objects.filter(comment=instance).delete()

    # Delete all notifications for the comment
    Notification.objects.filter(comment=instance).delete()

    # Update idea
    update_last_idea_activity(instance.idea)
    update_comment_count(instance.idea)


@receiver(post_save, sender=Vote)
def idea_voted(sender, instance, created, **kwargs):
    if created:
        # Check membership
        try:
            member = Member.objects.get(user=instance.user, company=instance.idea.company)
        except:
            Member(user=instance.user, company=instance.idea.company).save()

        # Create activity
        Activity(company=instance.idea.company, idea=instance.idea, user=instance.user, action='idea_wanted').save()
        update_last_idea_activity(instance.idea)

        # Subscribe to this idea
        subscription, created = Subscription.objects.get_or_create(idea=instance.idea, user=instance.user)
        # Create notifications
        create_notification(instance.user, instance.idea, 'idea_wanted')
        # Send idea wanted email
        send_want_email(instance)    

    update_vote_count(instance.idea)


@receiver(post_delete, sender=Vote)
def idea_unvoted(sender, instance, **kwargs):
    update_vote_count(instance.idea)
    # Delete activity
    Activity.objects.filter(idea=instance.idea, user=instance.user, action='idea_wanted').delete()
    update_last_idea_activity(instance.idea)

    # Unsubcribe if user doesn't have any comments
    comments = Comment.objects.filter(idea=instance.idea, created_by=instance.user).exists()
    if not comments:
        subscription = Subscription.objects.filter(idea=instance.idea, user=instance.user)
        subscription.delete()    
        # Delete all user notifications for the idea
        Notification.objects.filter(idea=instance.idea, user=instance.user).delete()
        Notification.objects.filter(idea=instance.idea, created_by=instance.user).delete()


@receiver(post_save, sender=Idea)
def idea_added(sender, instance, created, **kwargs):
    if created:
        # Create activity
        Activity(company=instance.company, idea=instance, user=instance.created_by, action='idea_submitted').save()
        update_last_idea_activity(instance)

        if instance.imported:
            return

        # Author auto-votes!
        vote = Vote()
        vote.idea = instance 
        vote.user = instance.created_by
        vote.save()    

        # Subscribe to this idea
        subscription, created = Subscription.objects.get_or_create(idea=instance, user=instance.created_by)

        # Create notifications
        create_notification(instance.created_by, instance, 'idea_submitted')

        # Send email to admin
        notify_admin_for_new_idea(instance)
    else:
        if instance.deleted == True:
            # Delete all activities for the idea
            Activity.objects.filter(idea=instance).delete()
            # Delete all notifications for the idea
            Notification.objects.filter(idea=instance).delete()


@receiver(pre_save, sender=Idea)
def idea_pre_add(sender, instance, **kwargs):
    try:
        idea = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Idea is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if (instance.status and 
            not idea.status == instance.status): # Status has changed
            # Create activity
            activity = Activity(company=instance.company, idea=instance, status=instance.status, user=instance.edited_by, action='status_changed')
            activity.save()
            instance.last_activity = activity
            create_notification(instance.edited_by, instance, 'status_changed')
            # send_status_change_email(instance)   


@receiver(post_save, sender=Activity)
def new_activity(sender, instance, created, **kwargs):
    if created and instance.company.slack:
        try:
            slack_webhook = instance.company.slack['incoming_webhook']['url']
        except:
            return

        payload = {
            "username": "wantoo",
            "mrkdwn": True,
            "icon_url": "http://wantoo.io/wp-content/uploads/2015/02/favicon.png"
        }
        company_url = ''.join(['https://', get_current_site(None).domain, '/' + instance.company.slug + '/' ])
        idea_url = ''.join(['https://', get_current_site(None).domain, instance.idea.get_absolute_url()])

        text = "<%s|%s>" % (company_url + 'member/' + str(instance.user.id) + '/', instance.user.get_full_name() )
        if instance.action == 'idea_submitted':
            text += ' added'
        elif instance.action == 'comment_added':
            text += ' commented on'
        elif instance.action == 'idea_wanted':
            text += ' wants'
        elif instance.action == 'status_changed':
            text += ' updated the status to "' + instance.status.title + '" for'            
        text += ' the idea'
        text += " <%s|%s>" % (idea_url, instance.idea.title)

        if instance.action == 'comment_added':
            text += '\n&gt;' + instance.comment.comment      

        payload['text'] = text
        requests.post(slack_webhook, json.dumps(payload), headers={'content-type': 'application/json'})

    # Send wantoo platform notification for internal tracking
    if (get_current_site(None).domain == 'wantoo.io') and (instance.action == 'comment_added' or instance.action == 'idea_submitted'):
        slack_webhook = 'https://hooks.slack.com/services/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'

        payload = {
            "username": "wantoo",
            "mrkdwn": True,
            "icon_url": "http://wantoo.io/wp-content/uploads/2015/02/favicon.png"
        }
        company_url = ''.join(['https://', get_current_site(None).domain, '/' + instance.company.slug + '/' ])
        idea_url = ''.join(['https://', get_current_site(None).domain, instance.idea.get_absolute_url()])

        text = "<%s|%s>" % (company_url + 'member/' + str(instance.user.id) + '/', instance.user.get_full_name() )
        if instance.action == 'idea_submitted':
            text += ' added'
        elif instance.action == 'comment_added':
            text += ' commented on'
        elif instance.action == 'idea_wanted':
            text += ' wants'
        elif instance.action == 'status_changed':
            text += ' updated the status to "' + instance.status.title + '" for'            
        text += ' the idea'
        text += " <%s|%s>" % (idea_url, instance.idea.title)
        text += " at <%s|%s>" % (company_url, instance.company.title)

        if instance.action == 'comment_added':
            text += '\n&gt;' + instance.comment.comment      

        payload['text'] = text
        requests.post(slack_webhook, json.dumps(payload), headers={'content-type': 'application/json'})

