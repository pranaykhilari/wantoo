# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 15:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55, verbose_name=b'Company name')),
                ('logo_url', models.URLField(blank=True, default=b'http://wantoo.io/static/dashboard/img/company_logos/sample-logo.jpg', null=True)),
                ('color', models.CharField(blank=True, default=b'3284FF', max_length=7, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('slack', jsonfield.fields.JSONField(blank=True, null=True)),
                ('blank_home', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.CharField(blank=True, default=b"We'd love your feedback. Tell us what you want.", max_length=200, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='DarkLaunch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_tag', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_created_features', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='user_features', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dark Launch Code',
                'verbose_name_plural': 'Dark Launch Codes',
            },
        ),
        migrations.CreateModel(
            name='FeatureCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=55, null=True)),
                ('question', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_companies', to='users.Company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_featured_companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Featured Board',
                'verbose_name_plural': 'Featured Boards',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_members', to='users.Company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Membership',
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('casl', models.BooleanField(default=False)),
                ('email_comment', models.BooleanField(default=True)),
                ('email_want', models.BooleanField(default=False)),
                ('email_comment_on_want', models.BooleanField(default=True)),
                ('email_comment_on_comment', models.BooleanField(default=True)),
                ('email_digest', models.BooleanField(default=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to='users.Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Detail',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userdetail',
            unique_together=set([('user', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('user', 'company')]),
        ),
    ]
