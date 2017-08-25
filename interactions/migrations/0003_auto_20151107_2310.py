# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0002_auto_20151107_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbound',
            name='action',
            field=models.ForeignKey(blank=True, to='interactions.Action', null=True),
        ),
    ]
