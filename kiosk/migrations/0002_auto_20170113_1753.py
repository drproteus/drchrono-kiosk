# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kiosk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('office_name', models.CharField(max_length=200)),
                ('exit_kiosk_key', models.CharField(max_length=200)),
                ('doctor', models.ForeignKey(related_name='config', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='arrival',
            name='doctor',
            field=models.ForeignKey(related_name='arrival', default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
