# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20150207_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='title', unique_with=('author',), editable=False),
            preserve_default=True,
        ),
    ]
