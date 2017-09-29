from django.contrib import admin
from .models import Idea, Category, Activity, Notification, Subscription, Comment, Status


class IdeaAdmin(admin.ModelAdmin):
    list_filter = ('company',)
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title',)
    exclude = ['description','created_by',]
    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change): 
        if formset.model == Idea:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.created_by = request.user
                instance.save()
        else:
            formset.save()     


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'created_by')

class ActivityAdmin(admin.ModelAdmin):
    pass

class NotificationAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class StatusAdmin(admin.ModelAdmin):
    pass

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('idea', 'user', 'created_at', 'muted')

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
