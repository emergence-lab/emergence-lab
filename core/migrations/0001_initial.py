# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('full_name', models.CharField(max_length=255, verbose_name='full name', blank=True)),
                ('short_name', models.CharField(max_length=50, verbose_name='preferred name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='custom_user', related_name='custom_users', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'db_table': 'users',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('name', models.CharField(max_length=45, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', editable=False)),
                ('description', ckeditor.fields.RichTextField(verbose_name='description', blank=True)),
            ],
            options={
                'db_table': 'investigations',
                'verbose_name': 'investigation',
                'verbose_name_plural': 'investigations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'operators',
                'verbose_name': 'operator',
                'verbose_name_plural': 'operators',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('name', models.CharField(max_length=45, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', editable=False)),
                ('core', models.BooleanField(default=False, verbose_name='core project')),
                ('description', ckeditor.fields.RichTextField(verbose_name='description', blank=True)),
            ],
            options={
                'db_table': 'projects',
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='project_tracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_pi', models.BooleanField(default=False)),
                ('operator', models.ForeignKey(to='core.operator')),
                ('project', models.ForeignKey(to='core.Project')),
            ],
            options={
                'db_table': 'project_operator_tracking',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('project', models.ForeignKey(to='core.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'project_tracking',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='operator',
            name='projects',
            field=models.ManyToManyField(to='core.Project', through='core.project_tracking'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operator',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='core.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(related_query_name='user', related_name='users', to='core.Project', through='core.ProjectTracking', blank=True, help_text='Projects this user is tracking', verbose_name='tracked projects'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='custom_user', related_name='custom_users', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
