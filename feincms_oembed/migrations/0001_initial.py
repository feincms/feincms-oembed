# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CachedLookup'
        db.create_table('feincms_oembed_cachedlookup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('_response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('_httpstatus', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('max_age_seconds', self.gf('django.db.models.fields.PositiveIntegerField')(default=604800)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('feincms_oembed', ['CachedLookup'])

    def backwards(self, orm):
        # Deleting model 'CachedLookup'
        db.delete_table('feincms_oembed_cachedlookup')

    models = {
        'feincms_oembed.cachedlookup': {
            'Meta': {'object_name': 'CachedLookup'},
            '_httpstatus': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '604800'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['feincms_oembed']