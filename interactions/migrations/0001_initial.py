# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=50)),
                ('audio_file', models.FileField(null=True, upload_to=b'audio', blank=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inbound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=140)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('twilio_cid', models.CharField(max_length=200, blank=True)),
                ('action', models.ForeignKey(to='interactions.Action')),
            ],
        ),
        migrations.CreateModel(
            name='Outbound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('twilio_cid', models.CharField(max_length=200, blank=True)),
                ('action', models.ForeignKey(to='interactions.Action')),
            ],
        ),
        migrations.CreateModel(
            name='TwilioNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=20)),
                ('subscribed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='outbound',
            name='frm',
            field=models.ForeignKey(to='interactions.TwilioNumber'),
        ),
        migrations.AddField(
            model_name='outbound',
            name='to',
            field=models.ForeignKey(to='interactions.User'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='frm',
            field=models.ForeignKey(to='interactions.User'),
        ),
        migrations.AddField(
            model_name='inbound',
            name='to',
            field=models.ForeignKey(to='interactions.TwilioNumber'),
        ),
        migrations.AddField(
            model_name='action',
            name='twilio_number',
            field=models.ForeignKey(to='interactions.TwilioNumber'),
        ),
        migrations.AlterUniqueTogether(
            name='action',
            unique_together=set([('twilio_number', 'keyword')]),
        ),
    ]
