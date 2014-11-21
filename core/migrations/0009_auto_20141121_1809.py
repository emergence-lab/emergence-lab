# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141121_1741'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='processnode',
            unique_together=set([]),
        ),
    ]
