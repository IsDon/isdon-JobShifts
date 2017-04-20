# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 05:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=40)),
                ('desc', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(db_index=True, max_length=20)),
                ('status', models.IntegerField(choices=[(1, 'Open'), (2, 'Filled'), (3, 'Inviting'), (4, 'Reviewing'), (5, 'Cancelled')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(db_index=True)),
                ('time_end', models.DateTimeField(db_index=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Job_Shift', related_query_name='Job_Shift', to='jobs.Job')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='shift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Shift_Position', related_query_name='Shift_Position', to='jobs.Shift'),
        ),
        migrations.AddField(
            model_name='position',
            name='staff_filling',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
