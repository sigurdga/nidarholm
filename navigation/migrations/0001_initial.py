# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Link'
        db.create_table('navigation_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['navigation.Link'])),
            ('older_sibling', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='younger_sibling', null=True, to=orm['navigation.Link'])),
        ))
        db.send_create_signal('navigation', ['Link'])


    def backwards(self, orm):
        
        # Deleting model 'Link'
        db.delete_table('navigation_link')


    models = {
        'navigation.link': {
            'Meta': {'object_name': 'Link'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'older_sibling': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'younger_sibling'", 'null': 'True', 'to': "orm['navigation.Link']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['navigation.Link']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['navigation']
