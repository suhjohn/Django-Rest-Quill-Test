# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 10:13
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeltaOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('insert_value', models.TextField(blank=True, null=True)),
                ('image_insert_value', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('video_insert_value', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('attributes_value', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='answer')),
            ],
        ),
        migrations.CreateModel(
            name='QuillPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_html', models.TextField(blank=True, null=True)),
                ('content_preview_html', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='deltaoperation',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delta_operation_set', to='djangorestquill.QuillPost'),
        ),
    ]
