# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0005_auto_20170113_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrival',
            name='patient_photo',
            field=models.CharField(default=b'http://placekitten.com/g/100/100', max_length=500),
        ),
    ]
