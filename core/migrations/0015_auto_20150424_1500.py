# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_processtemplate_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processtemplate',
            name='process',
            field=models.ForeignKey(related_query_name='process', related_name='process', to='core.Process'),
            preserve_default=True,
        ),
    ]
