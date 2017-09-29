# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from django.conf import settings
from django.contrib.auth.models import User
from users.models import UserDetail

from django.contrib.auth.hashers import make_password


def add_wantoo_bot(apps, schema_editor):

	User = apps.get_model(settings.AUTH_USER_MODEL)
	UserDetail = apps.get_model('users', 'UserDetail')

	print 'Creating Wantoo Bot User...'
	try:
		wantoo_bot = User.objects.get(email='bot@wantoo.io')
		print 'Wantoobot already exists...'
	except:
		#Doesn't work all the time...
		# wantoo_bot = User.objects.create_user(username='wantoo-bot',
		#                          email='bot@wantoo.io',
		#                          password='2i8oaKhwbeTc',
		#                          first_name="~ WANTOOBOT",
		#                          last_name="~",
		#                          is_staff=True,
		#                          is_superuser=True)
		# User = apps.get_registered_model('auth', 'User')
	    wantoo_bot = User(
			username='wantoo-bot',
			email='bot@wantoo.io',
			password=make_password('2i8oaKhwbeTc'),
			is_superuser=True,
			is_staff=True,
			first_name="~ WANTOOBOT",
			last_name="~",
	    )
	    wantoo_bot.save()
	    print 'Wantoobot Created!'
	print 'Done!'

	print 'Adding UserDetail to Wantoo Bot...'
	try: 
		user_detail = UserDetail()
		user_detail.user = wantoo_bot
		user_detail.casl = True
		user_detail.save()
		print 'UserDetail created!'
	except:
		print 'UserDetail already exists...'
	print 'Done!'


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_company_deleted'),
    ]

    operations = [
    	migrations.RunPython(add_wantoo_bot),
    ]
