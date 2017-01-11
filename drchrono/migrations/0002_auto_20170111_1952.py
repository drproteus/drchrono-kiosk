# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='birthdayalert',
            old_name='custom_body',
            new_name='custom_email_body',
        ),
        migrations.AddField(
            model_name='birthdayalert',
            name='custom_text_body',
            field=models.CharField(default='', max_length=160),
            preserve_default=False,
        ),
    ]
