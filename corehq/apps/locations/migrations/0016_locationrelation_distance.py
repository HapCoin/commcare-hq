# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-30 18:36
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0015_create_related_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationrelation',
            name='distance',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]