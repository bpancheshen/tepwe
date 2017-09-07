# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crk_drill', '0005_auto_20170907_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='trans_anim',
        ),
        migrations.AddField(
            model_name='tag',
            name='clitic',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='compound',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='connegative',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='demtype',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='imptype',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='language',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='nametype',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='numeraltype',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='passive',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='punctuation',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='reflexivepossessive',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='syntax',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='tag',
            name='transitivity_animacy',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='animacy',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='attributive',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='case',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='derivation',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='tag',
            name='distance',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='tag',
            name='gender',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='grade',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='tag',
            name='infinite',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='tag',
            name='intentional_definite',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='mode',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='tag',
            name='mood',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='number',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='object',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='tag',
            name='personnumber',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='tag',
            name='polarity',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='tag',
            name='possessive',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='tag',
            name='preverb',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='tag',
            name='subclass',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tense',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]