# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 20:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mypet', '0005_auto_20180310_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypetsimage',
            name='mypets',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mypet.Mypets'),
        ),
    ]
