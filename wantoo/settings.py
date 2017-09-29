import os, socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hostname = socket.gethostname()
print hostname

SECRET_KEY = '&ejm*brf^7nn1rhoscwmqe4p%yl7$umml9q5%=5wt)(itisoqy'
STRIPE_SECRET_KEY = 'sk_test_tDsqOUGEbZI8HSi7zMdiIpra'
STRIPE_PUBLISHABLE_KEY = 'pk_test_YtDO42QyIRlajJmacDiD0EJr'
INTERCOM_SECRET_KEY = 'Setgpw5pN2qP7LtMfGGsQEXu596kK9YInpUOrrBN'
INTERCOM_APP_ID = 'qiwo2zc2'
DEBUG = True
X_FRAME_OPTIONS = 'DENY'

# Application definition

INSTALLED_APPS = (
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.algoliasearch',
    'rest_framework',
    'rest_framework_swagger',
    'bootstrap3',
    'djrill',
    'idea',
    'users',
    'integrations',
    'staff',
    'debug_toolbar',
    'landing',
    'webpack_loader',
    'zebra',
    'stripe',
    'intercom',
    'django_bleach'


)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware', # for xss prevention
    'django.middleware.clickjacking.XFrameOptionsMiddleware', #clickjacking attack prevention
)

ROOT_URLCONF = 'wantoo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wantoo.context_processors.global_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'wantoo.wsgi.application'

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

####################################################################
# DATABASE
####################################################################

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'abcd',
        'USER': 'postgres',
        'PASSWORD': 'tudip123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
SSLIFY_DISABLE = True
if hostname.find('.local') != -1:
    DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, '../emails/')
    SSLIFY_DISABLE = True
    print 'debug hostname on'
else:
    DEBUG = True
    SSLIFY_DISABLE = True
    # MIDDLEWARE_CLASSES += ('sslify.middleware.SSLifyMiddleware',)
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    ###################################################################
    # EMAIL SETTINGS
    ###################################################################
    MANDRILL_API_KEY = "uMFI0_nz5K7bUBXefnjoPg"
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    SERVER_EMAIL = 'hello@wantoo.io'
    DEFAULT_FROM_EMAIL = 'wantoo <hello@wantoo.io>'
    print 'debug on'

# G_Mauli_Jadhav_QQeS

import dj_database_url

database_url = 'postgres://postgres:tudip123@localhost:5432/abcd'
DATABASES['default'] = dj_database_url.parse(database_url)

####################################################################
# ALLAUTH CONF
####################################################################

LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1000
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[wantoo] "
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_USER_DISPLAY = lambda user: user.email
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_SIGNUP_FORM_CLASS = 'users.models.SignupForm'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/?next=/dashboard/'
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_ADAPTER = 'users.adapter.MyAccountAdapter'

ALGOLIA = {
    'APPLICATION_ID': 'IQKHNBSCI3',
    'API_KEY': '9a6e17bceb91c1aec248d9dc8055996e',
}

try:
    ALGOLIA_APP_ID = 'IQKHNBSCI3'
    ALGOLIA_SEARCH_KEY = '1324eef69a1c67965aa847bde6984f66'
except:
    ALGOLIA_APP_ID = ''
    ALGOLIA_SEARCH_KEY = ''

MIXPANEL_KEY = '6ed42d865a903fbd2a0dd2b1dee33123'

SWAGGER_SETTINGS = {
    'is_superuser': True,
    'info': {
        'description': '',
        'title': 'wantoo Internal API documentation',
    },
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, '../webpack-stats.json'),
    }
}

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
         {'METHOD': 'oauth2',
          'SCOPE': ['email', 'public_profile'],
          'VERIFIED_EMAIL': True,
          'FIELDS': [
              'id',
              'email',
              'name',
              'first_name',
              'last_name',
              'verified',
              'locale',
              'timezone',
              'link',
              'gender',
              'updated_time'],
          'VERSION': 'v2.4'}}