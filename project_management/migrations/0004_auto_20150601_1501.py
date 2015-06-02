# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_literature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='abstract',
            field=core.models.fields.RichTextField(null=True, verbose_name='abstract', blank=True),
            preserve_default=True,
        ),
    ]
