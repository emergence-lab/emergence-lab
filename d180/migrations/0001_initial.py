# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Growth',
            fields=[
                ('process_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Process')),
                ('has_gan', models.BooleanField(default=False)),
                ('has_aln', models.BooleanField(default=False)),
                ('has_inn', models.BooleanField(default=False)),
                ('has_algan', models.BooleanField(default=False)),
                ('has_ingan', models.BooleanField(default=False)),
                ('other_material', models.CharField(max_length=50, blank=True)),
                ('orientation', models.CharField(default=b'0001', max_length=10)),
                ('is_template', models.BooleanField(default=False)),
                ('is_buffer', models.BooleanField(default=False)),
                ('has_pulsed', models.BooleanField(default=False)),
                ('has_superlattice', models.BooleanField(default=False)),
                ('has_mqw', models.BooleanField(default=False)),
                ('has_graded', models.BooleanField(default=False)),
                ('has_n', models.BooleanField(default=False)),
                ('has_p', models.BooleanField(default=False)),
                ('has_u', models.BooleanField(default=False)),
                ('investigations', models.ManyToManyField(related_query_name=b'growth', related_name='growths', to='core.Investigation')),
            ],
            options={
                'verbose_name': 'd180 growth',
                'verbose_name_plural': 'd180 growths',
            },
            bases=('core.process',),
        ),
        migrations.CreateModel(
            name='Platter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=45, verbose_name='name')),
                ('serial', models.CharField(max_length=20, verbose_name='serial number', blank=True)),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='date started')),
            ],
            options={
                'verbose_name': 'platter',
                'verbose_name_plural': 'platters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Readings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('layer', models.IntegerField()),
                ('layer_desc', models.CharField(max_length=45, blank=True)),
                ('pyro_out', models.DecimalField(max_digits=7, decimal_places=2)),
                ('pyro_in', models.DecimalField(max_digits=7, decimal_places=2)),
                ('ecp_temp', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tc_out', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tc_in', models.DecimalField(max_digits=7, decimal_places=2)),
                ('motor_rpm', models.DecimalField(max_digits=7, decimal_places=2)),
                ('gc_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('gc_position', models.DecimalField(max_digits=7, decimal_places=2)),
                ('voltage_in', models.DecimalField(max_digits=7, decimal_places=2)),
                ('voltage_out', models.DecimalField(max_digits=7, decimal_places=2)),
                ('current_in', models.DecimalField(max_digits=7, decimal_places=2)),
                ('current_out', models.DecimalField(max_digits=7, decimal_places=2)),
                ('top_vp_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('hydride_inner', models.DecimalField(max_digits=7, decimal_places=2)),
                ('hydride_outer', models.DecimalField(max_digits=7, decimal_places=2)),
                ('alkyl_flow_inner', models.DecimalField(max_digits=7, decimal_places=2)),
                ('alkyl_push_inner', models.DecimalField(max_digits=7, decimal_places=2)),
                ('alkyl_flow_middle', models.DecimalField(max_digits=7, decimal_places=2)),
                ('alkyl_push_middle', models.DecimalField(max_digits=7, decimal_places=2)),
                ('alkyl_flow_outer', models.DecimalField(max_digits=7, decimal_places=2)),
                ('alkyl_push_outer', models.DecimalField(max_digits=7, decimal_places=2)),
                ('n2_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('h2_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('nh3_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('hydride_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmga1_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmga1_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmga2_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmga2_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tega2_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tega2_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmin1_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmin1_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmal1_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmal1_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('cp2mg_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('cp2mg_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('cp2mg_dilution', models.DecimalField(max_digits=7, decimal_places=2)),
                ('silane_flow', models.DecimalField(max_digits=7, decimal_places=2)),
                ('silane_dilution', models.DecimalField(max_digits=7, decimal_places=2)),
                ('silane_mix', models.DecimalField(max_digits=7, decimal_places=2)),
                ('silane_pressure', models.DecimalField(max_digits=7, decimal_places=2)),
                ('growth', models.ForeignKey(to='d180.Growth')),
            ],
            options={
                'verbose_name': 'reading',
                'verbose_name_plural': 'readings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecipeLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('layer_num', models.IntegerField()),
                ('loop_num', models.IntegerField()),
                ('loop_repeats', models.IntegerField()),
                ('time', models.IntegerField()),
                ('cp2mg_flow', models.IntegerField()),
                ('tmin1_flow', models.IntegerField()),
                ('tmin2_flow', models.IntegerField()),
                ('tmga1_flow', models.IntegerField()),
                ('tmga2_flow', models.IntegerField()),
                ('tmal1_flow', models.IntegerField()),
                ('tega1_flow', models.IntegerField()),
                ('cp2mg_press', models.IntegerField()),
                ('tmin_press', models.IntegerField()),
                ('tmin2_press', models.IntegerField()),
                ('tmga1_press', models.IntegerField()),
                ('tmga2_press', models.IntegerField()),
                ('tmal1_press', models.IntegerField()),
                ('tega1_press', models.IntegerField()),
                ('cp2mg_push', models.IntegerField()),
                ('hyd_outer', models.IntegerField()),
                ('hyd_inner', models.IntegerField()),
                ('top_vp', models.IntegerField()),
                ('ring_purge', models.IntegerField()),
                ('alk_inj_press', models.IntegerField()),
                ('alk_diff_press', models.IntegerField()),
                ('alk_inj_push', models.IntegerField()),
                ('alk_vent_push', models.IntegerField()),
                ('motor_rpm', models.IntegerField()),
                ('sub_temp_outer', models.IntegerField()),
                ('sub_temp_inner', models.IntegerField()),
                ('n2_flow', models.IntegerField()),
                ('gc_press', models.IntegerField()),
                ('h2_flow', models.IntegerField()),
                ('nh3_flow', models.IntegerField()),
                ('sih4_flow', models.IntegerField()),
                ('spare_1', models.IntegerField()),
                ('sih4_push', models.IntegerField()),
                ('sih4_dd', models.IntegerField()),
                ('sih4_press', models.IntegerField()),
                ('gc_purge', models.IntegerField()),
                ('alk_outer', models.IntegerField()),
                ('alk_middle', models.IntegerField()),
                ('alk_inner', models.IntegerField()),
                ('hyd_line_press', models.IntegerField()),
                ('tmin1_mol_frac', models.IntegerField()),
                ('tmin2_mol_frac', models.IntegerField()),
                ('nh3_cond', models.IntegerField()),
                ('h2n2_switch', models.IntegerField()),
                ('alk_push_inner', models.IntegerField()),
                ('alk_push_middle', models.IntegerField()),
                ('alk_push_outer', models.IntegerField()),
                ('growth', models.ForeignKey(to='d180.Growth')),
            ],
            options={
                'verbose_name': 'layer',
                'verbose_name_plural': 'layers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cp2mg', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmin1', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmin2', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmga1', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmga2', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tmal1', models.DecimalField(max_digits=7, decimal_places=2)),
                ('tega1', models.DecimalField(max_digits=7, decimal_places=2)),
                ('nh3', models.DecimalField(max_digits=9, decimal_places=2)),
                ('sih4', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
            options={
                'verbose_name': 'source entry',
                'verbose_name_plural': 'source entries',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='growth',
            name='platter',
            field=models.ForeignKey(to='d180.Platter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='growth',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
