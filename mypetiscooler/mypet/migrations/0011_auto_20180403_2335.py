# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-04 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mypet', '0010_auto_20180403_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypetsimage',
            name='mypets',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypet.Mypets'),
        ),
        migrations.AlterField(
            model_name='petbattleimages',
            name='image1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='petbattleimages',
            name='image2',
            field=models.CharField(max_length=100),
        ),
    ]
