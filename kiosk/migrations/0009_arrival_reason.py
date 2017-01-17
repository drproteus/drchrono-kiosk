# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0008_auto_20170114_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='reason',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
