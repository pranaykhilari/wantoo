from django.apps import AppConfig
from django.contrib import algoliasearch

from .index import IdeaIndex

class IdeaConfig(AppConfig):
    name = 'idea'

    def ready(self):
        Idea = self.get_model('Idea')
        algoliasearch.register(Idea, IdeaIndex)

