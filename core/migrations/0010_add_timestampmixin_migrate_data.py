# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


def migrate_project_time_data(apps, schema_editor):
    Project = apps.get_model('core', 'project')
    for project in Project.objects.all():
        if project.start_date is not None:
            project.created = project.start_date

        if project.status_changed is not None:
            project.modified = project.status_changed
        else:
            project.modified = project.created
        project.save()


def reverse_migrate_project_time_data(apps, schema_editor):
    Project = apps.get_model('core', 'project')
    for project in Project.objects.all():
        if project.created is not None:
            project.start_date = project.created
            project.save()


def migrate_investigation_time_data(apps, schema_editor):
    Investigation = apps.get_model('core', 'investigation')
    for investigation in Investigation.objects.all():
        if investigation.start_date is not None:
            investigation.created = investigation.start_date

        if investigation.status_changed is not None:
            investigation.modified = investigation.status_changed
        else:
            investigation.modified = investigation.created
        investigation.save()


def reverse_migrate_investigation_time_data(apps, schema_editor):
    Investigation = apps.get_model('core', 'investigation')
    for investigation in Investigation.objects.all():
        if investigation.created is not None:
            investigation.start_date = investigation.created
            investigation.save()



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_migrate_user_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigation',
            name='created',
            field=models.DateTimeField(default=timezone.now(), verbose_name='date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investigation',
            name='modified',
            field=models.DateTimeField(default=timezone.now(), verbose_name='date modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_investigation_time_data, reverse_migrate_investigation_time_data),
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=timezone.now(), verbose_name='date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='modified',
            field=models.DateTimeField(default=timezone.now(), verbose_name='date modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_project_time_data, reverse_migrate_project_time_data),
    ]
