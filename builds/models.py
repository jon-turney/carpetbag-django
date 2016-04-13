# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django_unixdatetimefield import UnixDateTimeField

class Jobs(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False)
    srcpkg = models.TextField(blank=True, null=False)
    status = models.TextField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    buildlog = models.TextField(blank=True, null=True)
    built = models.BooleanField(blank=False, null=False)
    valid = models.BooleanField(blank=False, null=False)
    start_timestamp = UnixDateTimeField(blank=True, null=False)
    end_timestamp = UnixDateTimeField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'jobs'
