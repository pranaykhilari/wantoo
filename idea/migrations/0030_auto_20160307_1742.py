# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0029_idea_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='description',
            field=models.TextField(blank=True, verbose_name=b'Description', validators=[django.core.validators.MaxLengthValidator(5000)]),
        ),
    ]
