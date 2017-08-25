# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0003_auto_20151107_2310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inbound',
            old_name='twilio_cid',
            new_name='twilio_sid',
        ),
        migrations.RenameField(
            model_name='outbound',
            old_name='twilio_cid',
            new_name='twilio_sid',
        ),
    ]
