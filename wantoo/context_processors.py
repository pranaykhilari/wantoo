from django.conf import settings

def global_settings(request):
    return {
        'intercom_app_id' : settings.INTERCOM_APP_ID,
        'intercom_secret_key' : settings.INTERCOM_SECRET_KEY
    }