# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crk_drill', '0007_auto_20170907_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemma',
            name='translation',
            field=models.CharField(default='add trans', max_length=40),
            preserve_default=False,
        ),
    ]