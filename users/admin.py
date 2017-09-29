from .models import UserDetail
from django.contrib import admin
from .models import Company, Member, DarkLaunch


class UserDetailAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    # list_display = ('user', 'company', 'get_date_joined')
    def get_date_joined(self, obj):
        return obj.user.date_joined    
admin.site.register(UserDetail, UserDetailAdmin)


class DarkLaunchAdmin(admin.ModelAdmin):
    search_fields = ('feature_tag',)
    list_display = ('feature_tag', 'created_by', 'created_at')
admin.site.register(DarkLaunch, DarkLaunchAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    exclude = ['theme', 'phone',]
admin.site.register(Company, CompanyAdmin)


class MemberAdmin(admin.ModelAdmin):
    list_filter = ('company',)
admin.site.register(Member, MemberAdmin)


