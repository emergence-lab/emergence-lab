# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import simulations.models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0005_auto_20141216_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='file_path',
            field=models.FileField(help_text=b'ZIP File with all simulation data', storage=simulations.models.FixedS3BotoStorage(querystring_expire=600, querystring_auth=True, acl=b'private'), null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='investigations',
            field=models.ManyToManyField(to='core.Investigation'),
            preserve_default=True,
        ),
    ]
