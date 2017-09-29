#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import random, string, datetime, unicodedata, re
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode, force_unicode
from urlparse import urljoin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import hashlib


def SlugifyUnicode(value, separator='-'):
    value = value.replace(u'\u0131', 'i')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())

    return mark_safe(re.sub('[-\s]+', separator, value))


def SlugifyUniquely(value, model, slugfield="slug", separator='-'):
        """Returns a slug on a name which is unique within a model's table

        This code suffers a race condition between when a unique
        slug is determined and when the object with that slug is saved.
        It's also not exactly database friendly if there is a high
        likelyhood of common slugs being attempted.

        A good usage pattern for this code would be to add a custom save()
        method to a model with a slug field along the lines of:

                from django.template.defaultfilters import slugify

                def save(self):
                    if not self.id:
                        # replace self.name with your prepopulate_from field
                        self.slug = SlugifyUniquely(self.name, self.__class__)
                super(self.__class__, self).save()

        Original pattern discussed at
        http://www.b-list.org/weblog/2006/11/02/django-tips-auto-populated-fields
        """
        value = value[:70]
        value = SlugifyUnicode(value)
        
        suffix = 0
        potential = base = slugify(value)
        while True:
                if suffix:
                        potential = separator.join([base, str(suffix)])
                if not model.objects.filter(**{slugfield: potential}).count():
                        return potential
                # we hit a conflicting slug, so bump the suffix & try again
                suffix += 1



def _strip_tags(value):
    """
    Returns the given HTML with all tags stripped.
    This is a copy of django.utils.html.strip_tags, except that it adds some
    whitespace in between replaced tags to make sure words are not erroneously
    concatenated.
    """
    return re.sub(r'<[^>]*?>', ' ', force_unicode(value))


def get_ip_address(request):
    """ use requestobject to fetch client machine's IP Address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')    ### Real IP address of client Machine
    return ip   
 

def get_gravatar_url(user, size=80):
    WANTOO_LOGO = 'https://wantoo.io/static/dashboard/img/letters/default.png'
    if not user:
        return WANTOO_LOGO

    try:
        DEFAULT = 'https://wantoo.io/static/dashboard/img/letters/'+ user.first_name[0].lower().encode('utf-8') +'.png'
        url = 'https://www.gravatar.com/avatar/'  + hashlib.md5(user.email.lower().encode('utf-8')).hexdigest() + '?'
    except: 
        return WANTOO_LOGO

    url += urlencode([

        ('d', DEFAULT)
    ])
    return url