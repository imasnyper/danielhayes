# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 00:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20170221_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 23, 0, 39, 59, 316679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 22, 0, 39, 59, 316637, tzinfo=utc), verbose_name='date published'),
        ),
    ]
