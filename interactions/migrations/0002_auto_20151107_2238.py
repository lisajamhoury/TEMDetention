# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inbound',
            old_name='frm',
            new_name='from_number',
        ),
        migrations.RenameField(
            model_name='inbound',
            old_name='to',
            new_name='to_number',
        ),
        migrations.RenameField(
            model_name='outbound',
            old_name='frm',
            new_name='from_number',
        ),
        migrations.RenameField(
            model_name='outbound',
            old_name='to',
            new_name='to_number',
        ),
        migrations.RemoveField(
            model_name='inbound',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='outbound',
            name='updated',
        ),
    ]
