# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0007_auto_20151128_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fallback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('body', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='twilionumber',
            name='fallback',
            field=models.ForeignKey(to='interactions.Fallback', null=True),
        ),
    ]
