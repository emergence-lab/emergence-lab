# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semscan',
            name='image',
        ),
        migrations.AddField(
            model_name='semscan',
            name='file',
            field=models.ImageField(max_length=150, null=True, upload_to=b'/Users/neilnewman/Documents/Development/wbg-django/wbg/../media', blank=True),
            preserve_default=True,
        ),
    ]
