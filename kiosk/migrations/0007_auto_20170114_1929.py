# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0006_auto_20170114_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrival',
            name='patient_photo',
            field=models.CharField(default=b'http://placekitten.com/g/200/200', max_length=500),
        ),
    ]
