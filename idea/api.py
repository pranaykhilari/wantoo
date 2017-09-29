from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import IdeaSerializer, CategorySerializer, CommentSerializer, VoteSerializer, NotificationSerializer, CompanySerializer, StatusSerializer
from .models import Idea, Category, Comment, Vote, Activity, Notification, Subscription, Status
from .views import has_admin_permission, allow_board_access
from users.models import Company, Member
from django.contrib.auth.models import User

import json
import threading
from templated_emails.utils import send_templated_email
from django.contrib.auth.models import Group, Permission

from views import member_or_add

from django.core.exceptions import ValidationError


@api_view(['GET', 'POST'])
def ideas(request, company_slug):

    """
    View all the ideas for the company or create a new idea
    """       
    company = get_object_or_404(Company, slug=company_slug)


    if request.method == 'GET':
        ideas = Idea.objects.filter(company=company)
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseForbidden()  

        member_or_add(request.user, company)

        try:
            member = Member.objects.get(company=company, user=request.user)
            if member.blocked:
                return HttpResponseForbidden()  
        except:
            pass
        check = request.data.get('check')

        if check == "oneIdea":
            data = {
                'title': request.data.get('title').strip(),
                'created_by': request.user.pk,
            }

            if request.data.get('category'):
                data['category'] = request.data.get('category')

            if request.data.get('description'):
                data['description'] = request.data.get('description')

            if request.data.get('status'):
                data['status'] = request.data.get('status')
            else:
                data['status'] = None

            data['company'] = company.id
            serializer = IdeaSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = [];
            title= request.data.get('title')
            string = title.split('\n')
            for multiple_idea in string:
                if not multiple_idea == "":
                    data = {
                        'title': multiple_idea,
                        'created_by': request.user.pk,
                    }
                    if request.data.get('category'):
                        data['category'] = request.data.get('category')

                    if request.data.get('description'):
                        data['description'] = request.data.get('description')

                    if request.data.get('status'):
                        data['status'] = request.data.get('status')
                    else:
                        data['status'] = None

                    data['company'] = company.id
                    serializer = IdeaSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    response_data.append(serializer.data)
            print '***********',response_data
            return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def statuses(request, company_slug):
    """
    
    """       
    company = get_object_or_404(Company, slug=company_slug)

    if request.method == 'GET':
        statuses = Status.objects.filter(company=company)
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        data = {
            'title': request.data.get('title').strip(), 
            'created_by': request.user.pk,
        }

        if request.data.get('color'):
            data['color'] = request.data.get('color')

        if request.data.get('closed'):
            if request.data.get('closed') == 1 or request.data.get('closed') == '1':
                data['closed'] = True
            else:
                data['closed'] = False

        if request.data.get('order'):
            data['order'] = request.data.get('order')

        data['company'] = company.id 

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def idea_detail(request, company_slug, idea_id):
    """
    View idea details, or delete the idea
    """  
    idea = get_object_or_404(Idea, company__slug=company_slug, pk=idea_id)

    if request.method == 'GET':
        serializer = IdeaSerializer(idea)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not has_admin_permission(request.user, idea.company) and idea.created_by != request.user:
            return HttpResponseForbidden()  

        if request.data.get('title'):
            idea.title = request.data.get('title').strip()

        if request.data.get('description'):
            idea.description = request.data.get('description').strip()

        if request.data.get('category'):
            try:
                category = Category.objects.get(company__slug=company_slug, id=request.data.get('category'))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            idea.category = category
        idea.edited_by = request.user
        idea.save()        
        return Response(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if not has_admin_permission(request.user, idea.company) and idea.created_by != request.user:
            return HttpResponseForbidden()  
        idea.deleted = True
        idea.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def status_detail(request, company_slug, status_id):
    """
    
    """  
    idea_status = get_object_or_404(Status, pk=status_id)

    if request.method == 'GET':
        serializer = StatusSerializer(idea_status)
        return Response(serializer.data)

    elif request.method == 'PUT':

        if not has_admin_permission(request.user, idea_status.company) and idea_status.created_by != request.user:
            return HttpResponseForbidden()  

        if request.data.get('title'):
            idea_status.title = request.data.get('title').strip()

        if request.data.get('color'):
            idea_status.color = request.data.get('color')

        if request.data.get('closed'):
            if request.data.get('closed') == 1 or request.data.get('closed') == '1':
                idea_status.closed = True
            else:
                idea_status.closed = False

        try:
            idea_status.full_clean()
        except ValidationError as e:
            print 'VALIDATION for STATUS - FAILED'
            print e.message_dict
            pass
        idea_status.save()
        return Response(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':

        if not has_admin_permission(request.user, idea_status.company) and idea_status.created_by != request.user:
            return HttpResponseForbidden()  

        idea_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'POST'])
def idea_order(request, company_slug, idea_id):
    """
    Card Order for kanban
    """
    idea = get_object_or_404(Idea, company__slug=company_slug, pk=idea_id)

    if not has_admin_permission(request.user, idea.company) and idea.created_by != request.user:
        return HttpResponseForbidden()

    if request.data.get('order'):
        order = request.data.get('order')
        idea.order = order

    if request.data.get('status'):
        try: 
            idea_status = Status.objects.get(company__slug=company_slug, id=request.data.get('status'))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        idea.status = idea_status
    else:
        idea.status = None
    idea.edited_by = request.user
    try:
        idea.full_clean()
    except ValidationError as e:
        # Do something based on the errors contained in e.message_dict.
        # Display them to a user, or handle them programmatically.
        print 'VALIDATION for IDEA ORDER - FAILED'
        print e.message_dict
        pass
    idea.save()
    if request.data.get('changedIdeas'):
        UpdateIdeasOrderThread(request.data.get('changedIdeas')).start()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def status_order(request, company_slug, status_id):
    """
    Card Order for kanban. Currently not being used on the frontend...
    """
    status = get_object_or_404(Status, pk=status_id)

    if not has_admin_permission(request.user, status.company) and status.created_by != request.user:
        return HttpResponseForbidden()

    if request.data.get('order'):
        status.order = request.data.get('order')

    status.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def categories(request, company_slug):
    """
    View all the categories for the company or create a new one
    """       
    company = get_object_or_404(Company, slug=company_slug)

    if request.method == 'GET':
        categories = Category.objects.filter(company=company)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not has_admin_permission(request.user, company):
            return HttpResponseForbidden()   

        data = {'title': request.data.get('title'), 'created_by': request.user.pk}
        data['company'] = company.id 

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def notifications(request, company_slug):
    """
    Get the latest 10 notifications for the logged in user
    """       
    company = get_object_or_404(Company, slug=company_slug)

    if not request.user.is_authenticated():
        return HttpResponseForbidden()  

    if request.method == 'GET':
        notifications = Notification.objects.filter(idea__company=company, user=request.user)[:10]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST', 'DELETE'])
def votes(request, company_slug, idea_id):
    """
    Get all the votes for a specific idea, vote for an idea, or unvote the idea
    """
    company = get_object_or_404(Company, slug=company_slug)
    company = get_object_or_404(Company, slug=company_slug)
    member_exist = allow_board_access(request, company)
    if company.is_private and (not request.user.is_authenticated or not member_exist):
        override_base = "base_plain.html"
        return render(request, 'home.html', {
            'company': company,
            'member_exist': member_exist,
            'override_base': override_base
        })
    if not request.user.is_authenticated():
        return HttpResponseForbidden()        

    idea = get_object_or_404(Idea, company__slug=company_slug, id=idea_id)

    try:
        member = Member.objects.get(company=idea.company, user=request.user)
        if member.blocked:
            return HttpResponseForbidden()      
    except:
        pass

    if request.method == 'GET':
        votes = Vote.objects.filter(idea=idea)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            Vote.objects.get(idea__id=idea_id, user=request.user)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        if idea.merged_into:
            return HttpResponseForbidden()    

        member_or_add(request.user, idea.company)  

        data = {'idea': idea_id, 'user': request.user.pk}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if idea.merged_into:
            return HttpResponseForbidden()      
        
        vote = get_object_or_404(Vote, idea__id=idea_id, user=request.user)
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comments(request, company_slug, idea_id):
    """
    Get all the comments for the idea, or, post a new comment.
    """      
    idea = get_object_or_404(Idea, company__slug=company_slug, id=idea_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(idea=idea)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)  

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseForbidden()  

        member_or_add(request.user, idea.company)

        try:
            member = Member.objects.get(company=idea.company, user=request.user)
            if member.blocked:
                return HttpResponseForbidden()   
        except:
            pass

        data = {'idea': idea_id, 'comment':request.data.get('comment'), 'created_by': request.user.pk}
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET', 'DELETE'])
def comment_detail(request, company_slug, idea_id, comment_id):
    """
    View comment or delete
    """    
    comment = get_object_or_404(Comment, idea__id=idea_id, pk=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if not has_admin_permission(request.user, comment.idea.company) and comment.created_by != request.user:
            return HttpResponseForbidden()  

        try:
            member = Member.objects.get(company=comment.idea.company, user=request.user)
            if member.blocked:
                return HttpResponseForbidden()   
        except:
            pass

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def company(request, company_slug=None):
    """
    Save all initial company options dynamically from /company/ route
    """   

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    #if request.user.user_detail.company is None:

    if request.data.get('title'):
        data = {'title': request.data.get('title') }
        serializer = CompanySerializer(data=data)
        if serializer.is_valid():

            company = Company()
            company.title = data['title']
            company.created_by = request.user 
            company.save()

            ########Generating first idea by Wantoobot#########
            try:
                wantoo_bot = User.objects.get(email='bot@wantoo.io')
            except User.DoesNotExist:
               print 'Wantoobot Does not exists'
               raise

            idea = Idea()

            idea.title = 'This is a Test Idea'
            idea.description = "Welcome to Wantoo! Here's a test idea to help you explore your Idea Board's functionality.\n" \
                                "\nYou can vote for it by hitting the Want button.\n" \
                                "\nEdit this idea by hitting those three little dots next to the title.\n" \
                                "\nComment on it in the field below.\n" \
                                "\nShare this idea with others through Twitter, Facebook, or email via the buttons in the upper right.\n" \
                                "\nWhen you're in Management view, You can drag and drop this idea into different columns to instantly change its category.\n" \
                                "\nOnce you've gotten the hang of it, you can delete it and start adding real ideas of your own."

            idea.company = company
            idea.created_by = wantoo_bot
            idea.new = True
            idea.save()

            #############

            request.user.user_detail.company = company
            request.user.user_detail.save()

            slug = {'slug': company.slug }

            group = Group.objects.create(name=company.slug)
            perm = Permission.objects.get(codename='is_company_admin') 
            group.permissions.add(perm)

            #######
            usr_name = request.user.get_full_name()
            usr_email =  request.user.email
            usr_url =  'http://wantoo.io/'+ company.slug

            try:
                # send_templated_email([usr_email], "emails/sign_up", {
                #     'full_name': usr_name,
                #     'author_url': usr_url,
                # })
                send_templated_email(['help@wantoo.io'], "emails/new_board_admin", {
                    'full_name': usr_name,
                    'author_email': usr_email,
                    'author_url': usr_url,
                })
            except:
                return Response('Email didnt end...')
            #########                

            return Response( json.dumps(slug), status=status.HTTP_201_CREATED);
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    #else:

    company = get_object_or_404(Company, slug=company_slug)     

    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()
    else:

        if request.data.get('logo_url'):
            company.logo_url = request.data.get('logo_url').strip()

        if request.data.get('question'):
            company.question = request.data.get('question').strip()

        if request.data.get('color'):
            company.color = request.data.get('color').strip()

        company.save()     
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def send_mail(request, company_slug=None):

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, slug=company_slug) 

    if not has_admin_permission(request.user, company):
        return HttpResponseForbidden()   
    else:

        usr_name = request.user.get_full_name()
        usr_email =  request.user.email
        usr_url =  'http://wantoo.io/'+request.data.get('company')

        try:
            send_templated_email(["help@wantoo.io"], "emails/pro_admin", {
                'full_name': usr_name,
                'author_email': usr_email,
                'author_url': usr_url,
            })  
            return Response('Success email sent.')                 
        except:
            return Response('There was a problem sending the email...')

class UpdateIdeasOrderThread(threading.Thread):
    def __init__(self, changedIdeas, **kwargs):
        self.changedIdeas = json.loads(changedIdeas)
        super(UpdateIdeasOrderThread, self).__init__(**kwargs)

    def run(self):
        for changedIdea in self.changedIdeas:
            try:
                id = changedIdea["ideaId"]
                order_idea = Idea.objects.get(id=id)
                order_idea.order = changedIdea["order"]
                order_idea.save()
            except:
                print "idea not found"