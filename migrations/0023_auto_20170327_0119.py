# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whitehouse', '0022_auto_20170326_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stories',
            options={'ordering': ['-story_date'], 'verbose_name': 'story', 'verbose_name_plural': 'stories'},
        ),
        migrations.AddField(
            model_name='stories',
            name='presto_id',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Presto'),
        ),
    ]
