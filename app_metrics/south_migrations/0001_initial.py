# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Metric'
        db.create_table(u'app_metrics_metric', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('unique', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'app_metrics', ['Metric'])

        # Adding model 'MetricSet'
        db.create_table(u'app_metrics_metricset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('no_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_daily', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('send_weekly', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_monthly', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'app_metrics', ['MetricSet'])

        # Adding M2M table for field metrics on 'MetricSet'
        m2m_table_name = db.shorten_name(u'app_metrics_metricset_metrics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metricset', models.ForeignKey(orm[u'app_metrics.metricset'], null=False)),
            ('metric', models.ForeignKey(orm[u'app_metrics.metric'], null=False))
        ))
        db.create_unique(m2m_table_name, ['metricset_id', 'metric_id'])

        # Adding M2M table for field email_recipients on 'MetricSet'
        m2m_table_name = db.shorten_name(u'app_metrics_metricset_email_recipients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metricset', models.ForeignKey(orm[u'app_metrics.metricset'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['metricset_id', 'user_id'])

        # Adding model 'MetricItem'
        db.create_table(u'app_metrics_metricitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_metricitems', to=orm['auth.User'])),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('item_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('item_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app_metrics', ['MetricItem'])

        # Adding model 'MetricDay'
        db.create_table(u'app_metrics_metricday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'app_metrics', ['MetricDay'])

        # Adding model 'MetricWeek'
        db.create_table(u'app_metrics_metricweek', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'app_metrics', ['MetricWeek'])

        # Adding model 'MetricMonth'
        db.create_table(u'app_metrics_metricmonth', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'app_metrics', ['MetricMonth'])

        # Adding model 'MetricYear'
        db.create_table(u'app_metrics_metricyear', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'app_metrics', ['MetricYear'])

        # Adding model 'Gauge'
        db.create_table(u'app_metrics_gauge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60)),
            ('current_value', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=6)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 6, 12, 0, 0))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2017, 6, 12, 0, 0))),
        ))
        db.send_create_signal(u'app_metrics', ['Gauge'])


    def backwards(self, orm):
        # Deleting model 'Metric'
        db.delete_table(u'app_metrics_metric')

        # Deleting model 'MetricSet'
        db.delete_table(u'app_metrics_metricset')

        # Removing M2M table for field metrics on 'MetricSet'
        db.delete_table(db.shorten_name(u'app_metrics_metricset_metrics'))

        # Removing M2M table for field email_recipients on 'MetricSet'
        db.delete_table(db.shorten_name(u'app_metrics_metricset_email_recipients'))

        # Deleting model 'MetricItem'
        db.delete_table(u'app_metrics_metricitem')

        # Deleting model 'MetricDay'
        db.delete_table(u'app_metrics_metricday')

        # Deleting model 'MetricWeek'
        db.delete_table(u'app_metrics_metricweek')

        # Deleting model 'MetricMonth'
        db.delete_table(u'app_metrics_metricmonth')

        # Deleting model 'MetricYear'
        db.delete_table(u'app_metrics_metricyear')

        # Deleting model 'Gauge'
        db.delete_table(u'app_metrics_gauge')


    models = {
        u'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'batch_time_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_batchable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'timestamp_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'app_metrics.gauge': {
            'Meta': {'object_name': 'Gauge'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 6, 12, 0, 0)'}),
            'current_value': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 6, 12, 0, 0)'})
        },
        u'app_metrics.metric': {
            'Meta': {'object_name': 'Metric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'app_metrics.metricday': {
            'Meta': {'object_name': 'MetricDay'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'app_metrics.metricitem': {
            'Meta': {'object_name': 'MetricItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'item_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_metricitems'", 'to': u"orm['auth.User']"})
        },
        u'app_metrics.metricmonth': {
            'Meta': {'object_name': 'MetricMonth'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'app_metrics.metricset': {
            'Meta': {'object_name': 'MetricSet'},
            'email_recipients': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app_metrics.Metric']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'no_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_daily': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_monthly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_weekly': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'app_metrics.metricweek': {
            'Meta': {'object_name': 'MetricWeek'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'app_metrics.metricyear': {
            'Meta': {'object_name': 'MetricYear'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': u"orm['relationships.Relationship']", 'to': u"orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'relationships.relationship': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('from_user', 'to_user', 'status', 'site'),)", 'object_name': 'Relationship'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_users'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'relationships'", 'to': u"orm['sites.Site']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['relationships.RelationshipStatus']"}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_users'", 'to': u"orm['auth.User']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'})
        },
        u'relationships.relationshipstatus': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RelationshipStatus'},
            'from_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'symmetrical_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['app_metrics']