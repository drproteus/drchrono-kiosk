# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0004_auto_20170113_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='patient_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='patient_photo',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='arrival',
            name='scheduled_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 13, 21, 3, 29, 883265, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
