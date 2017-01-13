# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0002_auto_20170113_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='doctor',
            field=models.ForeignKey(related_name='configuration', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
