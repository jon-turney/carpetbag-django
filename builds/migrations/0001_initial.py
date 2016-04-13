# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, blank=True)),
                ('srcpkg', models.TextField(null=True, blank=True)),
                ('status', models.TextField(null=True, blank=True)),
                ('log', models.TextField(null=True, blank=True)),
                ('buildlog', models.TextField(null=True, blank=True)),
                ('built', models.IntegerField(null=True, blank=True)),
                ('valid', models.IntegerField(null=True, blank=True)),
                ('start_timestamp', models.IntegerField(null=True, blank=True)),
                ('end_timestamp', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'jobs',
                'managed': False,
            },
        ),
    ]
