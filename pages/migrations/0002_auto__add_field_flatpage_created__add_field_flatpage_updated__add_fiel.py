# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'FlatPage.created'
        db.add_column('pages_flatpage', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2010, 10, 30), blank=True), keep_default=False)

        # Adding field 'FlatPage.updated'
        db.add_column('pages_flatpage', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2010, 10, 30), blank=True), keep_default=False)

        # Adding field 'FlatPage.user'
        db.add_column('pages_flatpage', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)

        # Adding field 'FlatPage.group'
        db.add_column('pages_flatpage', 'group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, blank=True), keep_default=False)

        # Adding field 'FlatPage.text'
        db.add_column('pages_flatpage', 'text', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'FlatPage.text_html'
        db.add_column('pages_flatpage', 'text_html', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'FlatPage.created'
        db.delete_column('pages_flatpage', 'created')

        # Deleting field 'FlatPage.updated'
        db.delete_column('pages_flatpage', 'updated')

        # Deleting field 'FlatPage.user'
        db.delete_column('pages_flatpage', 'user_id')

        # Deleting field 'FlatPage.group'
        db.delete_column('pages_flatpage', 'group_id')

        # Deleting field 'FlatPage.text'
        db.delete_column('pages_flatpage', 'text')

        # Deleting field 'FlatPage.text_html'
        db.delete_column('pages_flatpage', 'text_html')


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
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pages.flatpage': {
            'Meta': {'object_name': 'FlatPage'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_markdown': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pages'", 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pages']