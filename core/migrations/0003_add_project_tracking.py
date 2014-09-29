# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('project', models.ForeignKey(to='core.project')),
                ('user', models.ForeignKey(to='core.User')),
            ],
            options={
                'db_table': 'project_tracking',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(related_query_name='user', related_name='users', to='core.project', through='core.ProjectTracking', blank=True, help_text='Projects this user is tracking', verbose_name='tracked projects'),
            preserve_default=True,
        ),
    ]
