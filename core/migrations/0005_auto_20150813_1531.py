# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0004_auto_20150809_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='member_group',
            field=models.ForeignKey(related_name='+', verbose_name='member_group', blank=True, to='auth.Group', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='owner_group',
            field=models.ForeignKey(related_name='+', verbose_name='owner_group', blank=True, to='auth.Group', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='viewer_group',
            field=models.ForeignKey(related_name='+', verbose_name='viewer_group', blank=True, to='auth.Group', null=True),
        ),
    ]
