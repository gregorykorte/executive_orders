# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 03:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_short', models.CharField(max_length=10)),
                ('agency_long', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Authorities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authority', models.CharField(max_length=50)),
                ('authority_section', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_date', models.DateField()),
                ('fr_pub', models.BooleanField()),
                ('fr_doc_no', models.CharField(max_length=20)),
                ('fr_date', models.DateField()),
                ('fr_url', models.URLField()),
                ('fr_pdf_url', models.URLField()),
                ('wh_url', models.URLField()),
                ('ucsb_url', models.URLField()),
                ('short_title', models.CharField(max_length=20)),
                ('long_title', models.CharField(max_length=256)),
                ('abstract', models.CharField(max_length=1000)),
                ('signed_location', models.CharField(max_length=100)),
                ('statement', models.CharField(max_length=5000)),
                ('subj_to_appropriations', models.BooleanField()),
                ('judicial_review', models.BooleanField()),
                ('authority', models.ManyToManyField(to='whitehouse.Authorities')),
            ],
        ),
        migrations.CreateModel(
            name='OrderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_type', models.CharField(max_length=5)),
                ('long_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='President',
            fields=[
                ('potus_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('party', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Stories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_title', models.CharField(max_length=100)),
                ('story_url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whitehouse.OrderType'),
        ),
        migrations.AddField(
            model_name='order',
            name='president',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whitehouse.President'),
        ),
        migrations.AddField(
            model_name='order',
            name='related_story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whitehouse.Stories'),
        ),
    ]