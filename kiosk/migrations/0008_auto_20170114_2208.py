# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0007_auto_20170114_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrival',
            name='doctor',
            field=models.ForeignKey(related_name='arrivals', to=settings.AUTH_USER_MODEL),
        ),
    ]
