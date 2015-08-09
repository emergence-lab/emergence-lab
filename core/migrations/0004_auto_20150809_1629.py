# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_history'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='datafile',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_core.datafile_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='substrate',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_core.substrate_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]
