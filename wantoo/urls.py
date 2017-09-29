from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView, TemplateView
from users import views as users_views
from idea import views as idea_views
from landing import views as landing_views
from staff import views as staff_views
from integrations import views as integrations_views
from idea import api as idea_api

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^join/$', RedirectView.as_view(url='/accounts/signup/?next=/my-boards/')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('rest_framework_swagger.urls')),
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),
]

urlpatterns += [
    url(r'^$', landing_views.home, name='home'),
    url(r'^team/$', landing_views.team, name='team'),
    url(r'^careers/$', landing_views.careers, name='careers'),
    url(r'^privacy/$', landing_views.privacy, name='privacy'),
    url(r'^terms-of-service/$', landing_views.terms_service, name='terms_service'),
    url(r'^terms-of-use/$', landing_views.terms_use, name='terms_use'),
    url(r'^lp/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)/$', landing_views.alt_signup, name='alt_signup'),
]


urlpatterns += [
    url(r'^staff/$', RedirectView.as_view(url='/staff/users/')),
    url(r'^staff/users/$', staff_views.home_user, name='staff_home_users'),
    url(r'^staff/users/export/$', staff_views.home_user_export, name='staff_home_user_export'),
    url(r'^staff/boards/$', staff_views.home_board, name='staff_home_boards'),
    url(r'^staff/boards/export$', staff_views.home_board_export, name='staff_home_boards_export'),
    url(r'^staff/featured/$', staff_views.featured_boards, name='staff_featured'),
    url(r'^staff/featured/delete/(?P<feature_id>\d+)/$', staff_views.featured_boards_delete, name='featured_boards_delete'),
    url(r'^staff/user/(?P<user_id>\d+)/$', staff_views.user_detail, name='staff_user_detail'),
    url(r'^staff/company/(?P<company_id>\d+)/$', staff_views.company_detail, name='staff_company_detail'),
    url(r'^staff/company/(?P<company_id>\d+)/ideas/$', staff_views.company_ideas, name='staff_company_ideas'),
    url(r'^staff/company/(?P<company_id>\d+)/activities/$', staff_views.company_activities, name='staff_company_activities'),
    url(r'^staff/company/(?P<company_id>\d+)/members/$', staff_views.company_members, name='staff_company_members'),
]

urlpatterns += [
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/twitter/$', integrations_views.search_twitter, name='search_twitter'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/slack/$', integrations_views.slack, name='slack'),
    url(r'^_slack_redirect/$', integrations_views.slack_redirect, name='slack_redirect'),
]

urlpatterns += [
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/$', idea_api.ideas, name='ideas'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/(?P<idea_id>[0-9]+)/$', idea_api.idea_detail, name='idea_detail'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/(?P<idea_id>[0-9]+)/order/$', idea_api.idea_order, name='idea_order'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/(?P<idea_id>[0-9]+)/votes/$', idea_api.votes, name='votes'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/(?P<idea_id>[0-9]+)/comments/$', idea_api.comments, name='comments'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/(?P<idea_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$', idea_api.comment_detail, name='comment_detail'),

    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/statuses/$', idea_api.statuses, name='statuses'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/statuses/(?P<status_id>[0-9]+)/$', idea_api.status_detail, name='status_detail'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/statuses/(?P<status_id>[0-9]+)/order/$', idea_api.status_order, name='status_order'),

    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/notifications/$', idea_api.notifications, name='notifications'),
    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/categories/$', idea_api.categories, name='categories'),

    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/company/$', idea_api.company, name='company'),
    url(r'^api/v1/company/$', idea_api.company, name='company'),


    url(r'^api/v1/(?P<company_slug>[a-zA-Z0-9_-]+)/sendmail/$', idea_api.send_mail, name='send_mail'),

]

urlpatterns += [
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/member/(?P<user_id>\d+)/$', users_views.member_detail, name='member_detail'),
    url(r'^accounts/preferences/$', users_views.preferences, name='preferences'),
    url(r'^accounts/preferences/notifications/$', users_views.notification_settings, name='notification_settings'),
    url(r'^accounts/preferences/subscription/$', users_views.subscription, name='subscription'),
    url(r'^accounts/preferences/subscription_payment/$', users_views.subscription_payment, name='subscription_payment'),
    url(r'^accounts/preferences/cancel_subscription/$', users_views.cancel_subscription, name='cancel_subscription'),
    url(r'^accounts/preferences/downgrade_subscription/$', users_views.downgrade_subscription, name='downgrade_subscription'),
    url(r'^accounts/preferences/upgrade_to_pro/$', users_views.upgrade_to_pro, name='upgrade_to_pro'),
    url(r'^accounts/preferences/update_subscription/$', users_views.update_subscription, name='update_subscription'),
    url(r'^my-boards/$', users_views.my_boards, name='my_boards'),
    url(r'^my-boards/closed/$', users_views.my_closed_boards, name='my_closed_boards'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/closed/admin/$', users_views.toggle_closed, name='toggle_closed'),
    url(r'^accounts/preferences/coupon/', users_views.stripecoupon, name='stripecoupon'),
    url(r'^stripe/webhook', users_views.stripe_webhook, name='stripe_webhook'),
    url(r'^<company_slug>[a-zA-Z0-9_-]$', users_views.private_login_view, name='private_login_view'),
]

urlpatterns += [
    url(r'^dashboard/$', idea_views.dashboard, name='dashboard'),
    url(r'^(?P<idea_id>\d+)/$', idea_views.idea_redirect, name='idea_redirect'),
    url(r'^ideas/reset-new/$', idea_views.reset_new_idea_status, name='reset_new_idea_status'),
    url(r'^all-activity/$', idea_views.all_activity, name='all_activity'),
    url(r'^mute/(?P<sub_key>[a-zA-Z0-9_-]+)/$', idea_views.mute_subscription, name='mute_subscription'),
    url(r'^welcome', idea_views.create_board, name='create_board'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/invite/$', idea_views.invite, name='invite'),
    url(r'resend_email', idea_views.resend_email, name='resend_email'),
    url(r'board_access', idea_views.board_access, name='board_access'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/activity/$', idea_views.activity, name='activity'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/notifications/$', idea_views.notifications, name='notifications'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/members/(?P<member_id>\d+)/block/$', idea_views.toggle_member_block, name='toggle_member_block'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/pending/(?P<member_id>\d+)/remove/$', idea_views.remove_invitee, name='remove_invitee'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/members/(?P<member_id>\d+)/admin/$', idea_views.toggle_admin_status, name='toggle_admin_status'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/settings/$', idea_views.company_settings, name='company_settings'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/search/$', idea_views.search, name='search'),

    # Idea ajax end-points FIXIT: depracating these soon
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/idea/move/$', idea_views._move_ideas, name='_move_ideas'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/idea/delete/$', idea_views._delete_ideas, name='_delete_ideas'),

    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/stats/$', idea_views.stats, name='stats'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/categories/$', idea_views.category_list, name='category_list'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/ideas/$', idea_views.idea_list, name='idea_list'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/members/$', idea_views.members, name='members'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/members/export/$', idea_views.export_members, name='export_members'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/statuses/$', idea_views.status_list, name='status_list'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/statuses/(?P<status_id>\d+)/edit/$', idea_views.edit_status, name='edit_status'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/statuses/add/$', idea_views.add_status, name='add_status'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/statuses/delete/$', idea_views.delete_status, name='delete_status'),

    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/add-idea/$', idea_views.add_idea, name='add_idea'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/idea/(?P<idea_id>\d+)/merge/$', idea_views.merge_idea, name='merge_idea'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/edit-idea/(?P<idea_id>\d+)/$', idea_views.edit_idea, name='edit_idea'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/delete-idea/$', idea_views.delete_idea, name='delete_idea'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/add-category/$', idea_views.add_category, name='add_category'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/import-uv/$', idea_views.import_uv, name='import_uv'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/export/$', idea_views.export_ideas, name='export_ideas'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/import/$', idea_views.import_ideas, name='import_ideas'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/delete-category/$', idea_views.delete_category, name='delete_category'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/(?P<idea_id>\d+)/(?P<idea_slug>[a-zA-Z0-9_-]+)/$', idea_views.idea_detail, name='idea_detail'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/category/(?P<category_id>\d+)/$', idea_views.category_ideas, name='category_ideas'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/category/(?P<category_id>\d+)/edit/$', idea_views.edit_category, name='edit_category'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/clear-notifications/$', idea_views.clear_notifications, name='clear_notifications'),

    # Should be the last one due to catch-all url structure
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/ideas/$', idea_views.company_forum, name='company_forum'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/$', idea_views.company_home, name='company_home'),

    #kanban
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/kanban/$', RedirectView.as_view(url='/%(company_slug)s/manage/feedback/'), name='kanban'),
    url(r'^(?P<company_slug>[a-zA-Z0-9_-]+)/manage/feedback/$', idea_views.kanban, name='main_kanban'),

]

urlpatterns += [
    url(r'^member/(?P<user_id>\d+)/$', users_views.member_detail, name='member_detail'),

    url(r'^signup/starter/$', users_views.SignupViewExt.as_view(
        plan_type = "starter",
        template_name = "account/main_signup.html"
    ), name="custom_signup_free"),
    url(r'^signup/pro/$', users_views.SignupViewExt.as_view(
        plan_type = "pro",
        template_name = "account/main_signup.html"
    ), name="custom_signup_pro"),
    url(r'^signup/premium/$', users_views.SignupViewExt.as_view(
        plan_type = "premium",
        template_name = "account/main_signup.html"
    ), name="custom_signup_premium"),
    url(r'^signup/pro/payment$', users_views.pro_plan, name='pro_subscription'),
    url(r'^signup/starter/payment$', users_views.starter_plan, name='starter_subscription'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
