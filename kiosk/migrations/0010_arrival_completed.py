# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0009_arrival_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
