# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whitehouse', '0028_auto_20170417_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deadline',
            name='deadline_order',
        ),
        migrations.AddField(
            model_name='order',
            name='deadline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='whitehouse.Deadline'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='related_story',
            field=models.ManyToManyField(blank=True, to='whitehouse.Stories'),
        ),
    ]
