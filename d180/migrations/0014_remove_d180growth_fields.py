# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0013_migrate_d180growth_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d180growth',
            name='has_algan',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_aln',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_gan',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_graded',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_ingan',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_inn',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_mqw',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_n',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_p',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_pulsed',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_superlattice',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='has_u',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='is_buffer',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='is_template',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='orientation',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='other_material',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='platter',
        ),
    ]
