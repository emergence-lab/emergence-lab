# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.process
import autoslug.fields
import mptt.fields
import core.models.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('full_name', models.CharField(max_length=255, verbose_name='full name', blank=True)),
                ('short_name', models.CharField(max_length=50, verbose_name='preferred name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='custom_user', related_name='custom_users', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('content_type', models.CharField(default='', max_length=200, blank=True, choices=[('', 'Unknown'), ('application/octet-stream', 'Binary File'), ('application/pdf', 'PDF File'), ('application/vnd.ms-excel', 'Excel File'), ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Excel File'), ('image/png', 'PNG Image'), ('image/bmp', 'BMP Image'), ('image/jpeg', 'JPEG Image'), ('image/tiff', 'TIFF Image'), ('image/gif', 'GIF Image'), ('text/plain', 'Plaintext File'), ('text/csv', 'CSV File')])),
                ('data', models.FileField(max_length=200, null=True, upload_to=core.models.process.get_file_path, blank=True)),
                ('state', models.CharField(default='raw', max_length=20, choices=[('raw', 'Raw'), ('cleaned', 'Cleaned'), ('extracted', 'Extracted'), ('analyzed', 'Analyzed'), ('other', 'Other')])),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_core.datafile_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
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
                ('description', core.models.fields.RichTextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'investigation',
                'verbose_name_plural': 'investigations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('due_date', models.DateField()),
                ('name', models.CharField(max_length=45, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', editable=False)),
                ('description', core.models.fields.RichTextField(verbose_name='description', blank=True)),
                ('investigation', models.ForeignKey(related_query_name='milestone', related_name='milestone', to='core.Investigation', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'milestone',
                'verbose_name_plural': 'milestones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MilestoneNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('note', core.models.fields.RichTextField(verbose_name='note', blank=True)),
                ('milestone', models.ForeignKey(related_query_name='note', related_name='note', to='core.Milestone', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('uuid_full', core.models.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('legacy_identifier', models.SlugField(max_length=100)),
                ('investigations', models.ManyToManyField(related_query_name='process', related_name='processes', to='core.Investigation')),
                ('milestones', models.ManyToManyField(related_query_name='milestone', related_name='processes', to='core.Milestone')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('uuid_full', core.models.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('piece', models.CharField(max_length=5)),
                ('number', models.IntegerField(default=1)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', to='core.ProcessNode', null=True)),
                ('process', models.ForeignKey(to='core.Process', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('name', models.CharField(max_length=50, blank=True)),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('process', models.ForeignKey(related_query_name='templates', related_name='templates', to='core.Process')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessType',
            fields=[
                ('type', models.SlugField(default='generic-process', max_length=100, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=255)),
                ('is_destructive', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
                ('scheduling_type', models.CharField(default='none', max_length=10, choices=[('none', 'None'), ('simple', 'Simple'), ('full', 'Full'), ('external', 'External')])),
            ],
            options={
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
                ('description', core.models.fields.RichTextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
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
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('process_tree', mptt.fields.TreeOneToOneField(null=True, to='core.ProcessNode')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('source', models.CharField(max_length=100, blank=True)),
                ('serial', models.CharField(max_length=25, blank=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_core.substrate_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('description', core.models.fields.RichTextField(verbose_name='description', blank=True)),
                ('due_date', models.DateField()),
                ('milestone', models.ForeignKey(related_query_name='task', related_name='task', to='core.Milestone', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sample',
            name='substrate',
            field=models.OneToOneField(to='core.Substrate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='process',
            name='type',
            field=models.ForeignKey(default='generic-process', to='core.ProcessType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='process',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='core.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datafile',
            name='process',
            field=models.ForeignKey(related_query_name='datafiles', related_name='datafiles', to='core.Process', null=True),
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
