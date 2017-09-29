# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0003_idea_vote_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='note',
            field=models.TextField(blank=True, verbose_name=b'Description', validators=[django.core.validators.MaxLengthValidator(300)]),
        ),
        migrations.AlterField(
            model_name='idea',
            name='title',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(70)]),
        ),
    ]
