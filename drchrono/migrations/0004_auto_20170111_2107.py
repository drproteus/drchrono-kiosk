# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0003_auto_20170111_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='cell_phone',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='middle_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='photo',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='zip_code',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
