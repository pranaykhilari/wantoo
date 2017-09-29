from django.contrib.algoliasearch import AlgoliaIndex

class IdeaIndex(AlgoliaIndex):
    fields = ('company_id', 'title', 'description', 'category', 'category_id', 'status', 'status_id', 'status_color', 'created_by_id', 'created_by_avatar', 'voted_users_id', 'last_activity_user_id', 'last_activity_user', 'last_activity_avatar', 'last_activity_action', 'last_activity_date', 'comment_count', 'vote_count', 'keywords')
    settings = {'attributesToIndex': ['title', 'description', 'keywords']}
    index_name = 'idea_index'
    should_index = 'non_deleted'
