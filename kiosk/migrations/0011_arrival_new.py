# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0010_arrival_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='new',
            field=models.BooleanField(default=True),
        ),
    ]
