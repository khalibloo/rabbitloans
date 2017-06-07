# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_loansettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='date_due',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='date_granted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='date_repaid',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
