# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whitehouse', '0017_auto_20170320_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_slug',
            field=models.SlugField(default='', max_length=256),
        ),
    ]
