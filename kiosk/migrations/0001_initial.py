# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arrival',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appointment_id', models.IntegerField()),
                ('patient_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seen_at', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
