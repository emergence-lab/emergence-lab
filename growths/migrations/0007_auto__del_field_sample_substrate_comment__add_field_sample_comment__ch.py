# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'sample.substrate_comment'
        db.delete_column('samples', 'substrate_comment')

        # Adding field 'sample.comment'
        db.add_column('samples', 'comment',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


        # Changing field 'sample.pocket'
        db.alter_column('samples', 'pocket', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):
        # Adding field 'sample.substrate_comment'
        db.add_column('samples', 'substrate_comment',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Deleting field 'sample.comment'
        db.delete_column('samples', 'comment')


        # Changing field 'sample.pocket'
        db.alter_column('samples', 'pocket', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'core.investigation': {
            'Meta': {'object_name': 'investigation', 'db_table': "u'investigations'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.project']", 'symmetrical': 'False'})
        },
        u'core.operator': {
            'Meta': {'object_name': 'operator', 'db_table': "u'operators'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'core.platter': {
            'Meta': {'object_name': 'platter', 'db_table': "u'platters'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'project', 'db_table': "u'projects'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'growths.growth': {
            'Meta': {'object_name': 'growth', 'db_table': "'growths'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'growth_number': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'has_algan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_alingan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_aln': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_gan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_ingan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_inn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_mqw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_n': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_superlattice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_u': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.investigation']"}),
            'is_buffer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.operator']"}),
            'orientation': ('django.db.models.fields.CharField', [], {'default': "'0001'", 'max_length': '10'}),
            'other_material': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'platter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.platter']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.project']"}),
            'reactor': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'run_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'growths.readings': {
            'Meta': {'object_name': 'readings', 'db_table': "'readings'"},
            'alkyl_flow_inner': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'alkyl_flow_middle': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'alkyl_flow_outer': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'alkyl_push_inner': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'alkyl_push_middle': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'alkyl_push_outer': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'cp2mg_dilution': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'cp2mg_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'cp2mg_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'current_in': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'current_out': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'gc_position': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'gc_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.growth']"}),
            'h2_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'hydride_inner': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'hydride_outer': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'hydride_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer': ('django.db.models.fields.IntegerField', [], {}),
            'layer_desc': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'motor_rpm': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'n2_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'nh3_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'pyro_in': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'pyro_out': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'silane_dilution': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'silane_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'silane_mix': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'silane_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tc_in': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tc_out': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tega2_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tega2_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmal1_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmal1_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmga1_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmga1_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmga2_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmga2_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmin1_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmin1_pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'top_vp_flow': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'voltage_in': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'voltage_out': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
        u'growths.recipe_layer': {
            'Meta': {'object_name': 'recipe_layer', 'db_table': "'recipe_layers'"},
            'alk_diff_press': ('django.db.models.fields.IntegerField', [], {}),
            'alk_inj_press': ('django.db.models.fields.IntegerField', [], {}),
            'alk_inj_push': ('django.db.models.fields.IntegerField', [], {}),
            'alk_inner': ('django.db.models.fields.IntegerField', [], {}),
            'alk_middle': ('django.db.models.fields.IntegerField', [], {}),
            'alk_outer': ('django.db.models.fields.IntegerField', [], {}),
            'alk_push_inner': ('django.db.models.fields.IntegerField', [], {}),
            'alk_push_middle': ('django.db.models.fields.IntegerField', [], {}),
            'alk_push_outer': ('django.db.models.fields.IntegerField', [], {}),
            'alk_vent_push': ('django.db.models.fields.IntegerField', [], {}),
            'cp2mg_flow': ('django.db.models.fields.IntegerField', [], {}),
            'cp2mg_press': ('django.db.models.fields.IntegerField', [], {}),
            'cp2mg_push': ('django.db.models.fields.IntegerField', [], {}),
            'gc_press': ('django.db.models.fields.IntegerField', [], {}),
            'gc_purge': ('django.db.models.fields.IntegerField', [], {}),
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.growth']"}),
            'h2_flow': ('django.db.models.fields.IntegerField', [], {}),
            'h2n2_switch': ('django.db.models.fields.IntegerField', [], {}),
            'hyd_inner': ('django.db.models.fields.IntegerField', [], {}),
            'hyd_line_press': ('django.db.models.fields.IntegerField', [], {}),
            'hyd_outer': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer_num': ('django.db.models.fields.IntegerField', [], {}),
            'loop_num': ('django.db.models.fields.IntegerField', [], {}),
            'loop_repeats': ('django.db.models.fields.IntegerField', [], {}),
            'motor_rpm': ('django.db.models.fields.IntegerField', [], {}),
            'n2_flow': ('django.db.models.fields.IntegerField', [], {}),
            'nh3_cond': ('django.db.models.fields.IntegerField', [], {}),
            'nh3_flow': ('django.db.models.fields.IntegerField', [], {}),
            'ring_purge': ('django.db.models.fields.IntegerField', [], {}),
            'sih4_dd': ('django.db.models.fields.IntegerField', [], {}),
            'sih4_flow': ('django.db.models.fields.IntegerField', [], {}),
            'sih4_press': ('django.db.models.fields.IntegerField', [], {}),
            'sih4_push': ('django.db.models.fields.IntegerField', [], {}),
            'spare_1': ('django.db.models.fields.IntegerField', [], {}),
            'sub_temp_inner': ('django.db.models.fields.IntegerField', [], {}),
            'sub_temp_outer': ('django.db.models.fields.IntegerField', [], {}),
            'tega1_flow': ('django.db.models.fields.IntegerField', [], {}),
            'tega1_press': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'tmal1_flow': ('django.db.models.fields.IntegerField', [], {}),
            'tmal1_press': ('django.db.models.fields.IntegerField', [], {}),
            'tmga1_flow': ('django.db.models.fields.IntegerField', [], {}),
            'tmga1_press': ('django.db.models.fields.IntegerField', [], {}),
            'tmga2_flow': ('django.db.models.fields.IntegerField', [], {}),
            'tmga2_press': ('django.db.models.fields.IntegerField', [], {}),
            'tmin1_flow': ('django.db.models.fields.IntegerField', [], {}),
            'tmin1_mol_frac': ('django.db.models.fields.IntegerField', [], {}),
            'tmin2_flow': ('django.db.models.fields.IntegerField', [], {}),
            'tmin2_mol_frac': ('django.db.models.fields.IntegerField', [], {}),
            'tmin2_press': ('django.db.models.fields.IntegerField', [], {}),
            'tmin_press': ('django.db.models.fields.IntegerField', [], {}),
            'top_vp': ('django.db.models.fields.IntegerField', [], {})
        },
        u'growths.sample': {
            'Meta': {'object_name': 'sample', 'db_table': "'samples'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.growth']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.sample']", 'null': 'True', 'blank': 'True'}),
            'piece': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'pocket': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'whole'", 'max_length': '20'}),
            'substrate_miscut': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'substrate_orientation': ('django.db.models.fields.CharField', [], {'default': "'0001'", 'max_length': '10'}),
            'substrate_serial': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'substrate_type': ('django.db.models.fields.CharField', [], {'default': "'sapphire'", 'max_length': '20'})
        },
        u'growths.serial_number': {
            'Meta': {'object_name': 'serial_number', 'db_table': "'serial_numbers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'growths.source': {
            'Meta': {'object_name': 'source', 'db_table': "'sources'"},
            'cp2mg': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nh3': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'sih4': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'tega1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmal1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmga1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmga2': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmin1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tmin2': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        }
    }

    complete_apps = ['growths']