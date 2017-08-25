# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0005_auto_20151108_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='twilionumber',
            name='alpha_id',
            field=models.BooleanField(default=False),
        ),
    ]
