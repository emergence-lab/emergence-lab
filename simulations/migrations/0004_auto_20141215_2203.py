# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0003_auto_20141215_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='file_path',
            field=models.FileField(null=True, upload_to=b'path', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='investigations',
            field=models.ManyToManyField(to='core.Investigation'),
            preserve_default=True,
        ),
    ]
