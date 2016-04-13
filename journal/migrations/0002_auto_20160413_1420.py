# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='title', unique_with=('author',), editable=False),
        ),
    ]
