# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Groupcategory'
        db.create_table('relations_groupcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('relations', ['Groupcategory'])

        # Adding model 'GroupProfile'
        db.create_table('relations_groupprofile', (
            ('groupcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.Groupcategory'])),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.Group'], unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('relations', ['GroupProfile'])

        # Adding model 'Role'
        db.create_table('relations_role', (
            ('groupprofile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.GroupProfile'])),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('relations', ['Role'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Groupcategory'
        db.delete_table('relations_groupcategory')

        # Deleting model 'GroupProfile'
        db.delete_table('relations_groupprofile')

        # Deleting model 'Role'
        db.delete_table('relations_role')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'relations.groupcategory': {
            'Meta': {'object_name': 'Groupcategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'relations.groupprofile': {
            'Meta': {'object_name': 'GroupProfile'},
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.Group']", 'unique': 'True'}),
            'groupcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Groupcategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'relations.role': {
            'Meta': {'object_name': 'Role'},
            'groupprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.GroupProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['relations']
