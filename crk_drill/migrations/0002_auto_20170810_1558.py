# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crk_drill', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='animacy',
        ),
        migrations.RemoveField(
            model_name='word',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='word',
            name='pos',
        ),
        migrations.AddField(
            model_name='lemma',
            name='animacy',
            field=models.CharField(default='null', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lemma',
            name='language',
            field=models.CharField(default='crk', max_length=5),
        ),
        migrations.AddField(
            model_name='lemma',
            name='pos',
            field=models.CharField(default='null', max_length=12),
            preserve_default=False,
        ),
    ]
