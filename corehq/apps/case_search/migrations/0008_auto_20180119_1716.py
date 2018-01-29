# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 17:16
from __future__ import absolute_import
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations

from corehq.sql_db.operations import HqRunPython


def update_es_mapping(*args, **kwargs):
    def _update_es_mapping():
        return call_command('update_es_mapping', 'case_search', noinput=True)
    return _update_es_mapping


class Migration(migrations.Migration):

    dependencies = [
        ('case_search', '0007_auto_20170522_1506'),
    ]

    operations = [
        HqRunPython(update_es_mapping)
    ]