# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-26 19:00
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations

from corehq.apps.smsbillables.management.commands.deactivate_grapevine_instance_fee_criteria import \
    deactivate_grapevine_instance_fee_criteria
from corehq.sql_db.operations import HqRunPython


def deactivate_grapevine_instance_fees(apps, schema_editor):
    deactivate_grapevine_instance_fee_criteria(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('smsbillables', '0016_smsgatewayfeecriteria_is_active'),
    ]

    operations = [
        HqRunPython(deactivate_grapevine_instance_fees),
    ]