# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whitehouse', '0023_auto_20170327_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='story_url',
            field=models.URLField(default=''),
        ),
    ]