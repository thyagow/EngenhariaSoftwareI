# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('data', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=200)),
                ('preco_inicial', models.FloatField()),
                ('preco_final', models.FloatField(default=models.FloatField())),
                ('data_inicio', models.DateTimeField(auto_now=True)),
                ('data_final', models.DateTimeField(default=None)),
                ('estado', models.IntegerField(default=0)),
                ('id_arrematante', models.IntegerField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('senha', models.CharField(max_length=100)),
                ('saldo', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='comitente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trabalho.Usuario'),
        ),
        migrations.AddField(
            model_name='lance',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trabalho.Produto'),
        ),
        migrations.AddField(
            model_name='lance',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trabalho.Usuario'),
        ),
    ]
