# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drchrono', '0002_auto_20170111_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drchrono_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('birthday', models.DateField()),
                ('email', models.CharField(max_length=200)),
                ('gender', models.CharField(default=b'', max_length=200)),
                ('zip_code', models.CharField(max_length=200)),
                ('cell_phone', models.CharField(max_length=200)),
                ('photo', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='birthdayalert',
            name='patient_id',
        ),
        migrations.AlterField(
            model_name='birthdayalert',
            name='birthday',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='birthdayalert',
            name='doctor',
            field=models.ForeignKey(related_name='patient_alert', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='birthdayalert',
            name='patient',
            field=models.ForeignKey(related_name='alert', default=0, to='drchrono.Patient'),
            preserve_default=False,
        ),
    ]
