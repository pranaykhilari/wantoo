# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_member_email_digest'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='question',
            field=models.CharField(default="We'd love your feedback. Tell us what you want.", max_length=200, null=True, blank=True),
        ),
    ]
