# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Instrument'
        db.create_table('instruments_instrument', (
            ('number', self.gf('django.db.models.fields.SmallIntegerField')(db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('instruments', ['Instrument'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Instrument'
        db.delete_table('instruments_instrument')
    
    
    models = {
        'instruments.instrument': {
            'Meta': {'object_name': 'Instrument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'})
        }
    }
    
    complete_apps = ['instruments']
