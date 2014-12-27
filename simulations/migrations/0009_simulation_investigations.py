# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20141222_1649'),
        ('simulations', '0008_auto_20141220_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='investigations',
            field=models.ManyToManyField(to='core.Investigation'),
            preserve_default=True,
        ),
    ]
