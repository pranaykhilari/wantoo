"""API Serializers

Module contains declarations for any Model serializers used by the idea.api module.
Purpose is to allow the datatypes to be served through JSON to the client, which is 
currently being handled by React for client rendering of the 'Idea List' and 
'Notifications'.

Naming conventions map to the appropriate modals.
"""


from rest_framework import serializers
from idea.models import Idea, Category, Comment, Vote, Notification, Company, Status
from idea.templatetags import mytags 


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ('id','title', 'description', 'company', 'vote_count', 'comment_count', 'created_by', 'category', 'status')

    def create(self, validated_data):
        idea = Idea(**validated_data)
        idea.save()
        return idea


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'title', 'company', 'color', 'closed', 'created_by', 'order')

    def create(self, validated_data):
        status = Status(**validated_data)
        status.save()
        return status


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title','company', 'created_by')


class NotificationSerializer(serializers.ModelSerializer):
    idea_id = serializers.CharField(source='idea.id', read_only=True)
    idea_title = serializers.CharField(source='idea.title', read_only=True)
    user_full_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    user_id = serializers.CharField(source='created_by.id', read_only=True)
    status_title = serializers.CharField(source='status.title', read_only=True)

    class Meta:
        model = Notification
        fields = ('idea_id', 'idea_title', 'user_full_name', 'user_id', 'status_title', 'avatar', 'seen', 'timesince', 'own_idea', 'action')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'idea', 'comment','created_by')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id','user','idea')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('title',)

