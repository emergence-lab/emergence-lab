# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_user_data(apps, schema_editor):
    OldUser = apps.get_model('auth', 'User')
    NewUser = apps.get_model('core', 'User')
    for user in OldUser.objects.all():
        NewUser.objects.create(id=user.id, username=user.username,
            password=user.password, email=user.email, is_active=user.is_active,
            is_superuser=user.is_superuser, is_staff=user.is_staff,
            last_login=user.last_login, date_joined=user.date_joined,
            full_name=user.first_name, short_name='')


def reverse_migrate_user_data(apps, schema_editor):
    NewUser = apps.get_model('core', 'User')
    NewUser.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_platter_end_date'),
    ]

    operations = [
        migrations.RunPython(migrate_user_data, reverse_migrate_user_data),
    ]
