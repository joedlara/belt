# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belty', '0004_auto_20170504_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='belty.Quote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='belty.User')),
            ],
        ),
    ]