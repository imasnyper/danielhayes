# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 21:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20170220_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='active',
        ),
    ]
