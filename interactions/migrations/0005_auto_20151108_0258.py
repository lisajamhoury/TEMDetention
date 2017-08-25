# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0004_auto_20151108_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='followup',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='outbound',
            name='followup_sent',
            field=models.BooleanField(default=False),
        ),
    ]
