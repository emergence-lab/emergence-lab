# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'afm.height'
        db.alter_column('afm', 'height', self.gf('django.db.models.fields.files.ImageField')(max_length=150, null=True))

        # Changing field 'afm.amplitude'
        db.alter_column('afm', 'amplitude', self.gf('django.db.models.fields.files.ImageField')(max_length=150, null=True))
        # Adding unique constraint on 'afm', fields ['growth', 'sample', 'scan_number', 'location']
        db.create_unique('afm', ['growth_id', 'sample_id', 'scan_number', 'location'])


    def backwards(self, orm):
        # Removing unique constraint on 'afm', fields ['growth', 'sample', 'scan_number', 'location']
        db.delete_unique('afm', ['growth_id', 'sample_id', 'scan_number', 'location'])


        # Changing field 'afm.height'
        db.alter_column('afm', 'height', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=150))

        # Changing field 'afm.amplitude'
        db.alter_column('afm', 'amplitude', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=150))

    models = {
        u'afm.afm': {
            'Meta': {'unique_together': "(('growth', 'sample', 'scan_number', 'location'),)", 'object_name': 'afm', 'db_table': "'afm'"},
            'amplitude': ('django.db.models.fields.files.ImageField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.growth']"}),
            'height': ('django.db.models.fields.files.ImageField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '45'}),
            'rms': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.sample']"}),
            'scan_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'size': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'zrange': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'})
        },
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
        u'growths.sample': {
            'Meta': {'object_name': 'sample', 'db_table': "'samples'"},
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.growth']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['growths.sample']", 'null': 'True', 'blank': 'True'}),
            'piece': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'pocket': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'whole'", 'max_length': '20'}),
            'substrate_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'substrate_miscut': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'substrate_orientation': ('django.db.models.fields.CharField', [], {'default': "'0001'", 'max_length': '10'}),
            'substrate_serial': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'substrate_type': ('django.db.models.fields.CharField', [], {'default': "'sapphire'", 'max_length': '20'})
        }
    }

    complete_apps = ['afm']