# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_processnode_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplitProcess',
            fields=[
                ('process_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Process')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
        migrations.AlterUniqueTogether(
            name='processnode',
            unique_together=set([('uid', 'tree_id')]),
        ),
    ]
