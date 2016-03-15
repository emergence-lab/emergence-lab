# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_processcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtype',
            name='creation_type',
            field=models.CharField(default='default', max_length=10, choices=[('default', 'Default'), ('custom', 'Custom')]),
        ),
    ]
