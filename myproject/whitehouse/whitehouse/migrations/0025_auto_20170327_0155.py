# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whitehouse', '0024_auto_20170327_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='story_url',
            field=models.URLField(),
        ),
    ]
