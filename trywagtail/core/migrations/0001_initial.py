# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('docker_container_exists', models.BooleanField(default=False)),
                ('docker_container_id', models.CharField(max_length=255)),
                ('docker_container_started', models.BooleanField(default=False)),
                ('docker_container_port', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docker_image_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='container',
            name='image',
            field=models.ForeignKey(to='trywagtail.Image'),
        ),
    ]
