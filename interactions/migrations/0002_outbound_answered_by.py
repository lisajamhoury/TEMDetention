# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outbound',
            name='answered_by',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
