# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mypet', '0007_auto_20180329_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='MypetsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photo/')),
            ],
        ),
        migrations.RemoveField(
            model_name='mypets',
            name='photo',
        ),
        migrations.AddField(
            model_name='mypetsimage',
            name='mypets',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mypet.Mypets'),
        ),
    ]
