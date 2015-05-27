# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_processtype'),
        ('d180', '0007_remove_d180growth_user_old'),
    ]

    operations = [
        migrations.CreateModel(
            name='D180GrowthInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_gan', models.BooleanField(default=False)),
                ('has_aln', models.BooleanField(default=False)),
                ('has_inn', models.BooleanField(default=False)),
                ('has_algan', models.BooleanField(default=False)),
                ('has_ingan', models.BooleanField(default=False)),
                ('other_material', models.CharField(max_length=50, blank=True)),
                ('orientation', models.CharField(default='0001', max_length=10)),
                ('is_template', models.BooleanField(default=False)),
                ('is_buffer', models.BooleanField(default=False)),
                ('has_pulsed', models.BooleanField(default=False)),
                ('has_superlattice', models.BooleanField(default=False)),
                ('has_mqw', models.BooleanField(default=False)),
                ('has_graded', models.BooleanField(default=False)),
                ('has_n', models.BooleanField(default=False)),
                ('has_p', models.BooleanField(default=False)),
                ('has_u', models.BooleanField(default=False)),
                ('platter', models.ForeignKey(to='d180.Platter')),
                ('process', models.OneToOneField(related_name='info', to='core.Process')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
