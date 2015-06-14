# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images/', verbose_name='character image')),
                ('mood', models.CharField(default=b'N', max_length=2, choices=[(b'N', b'Normal'), (b'M', b'Mad'), (b'A', b'Angry')])),
            ],
            options={
                'verbose_name': 'character',
                'verbose_name_plural': 'characters',
            },
        ),
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('utterance', models.TextField()),
                ('character', models.CharField(default=b'GP', max_length=2, choices=[(b'GP', b'Game Player'), (b'VC', b'Virtual Character')])),
                ('mood', models.CharField(default=b'N', max_length=2, null=True, blank=True, choices=[(b'N', b'Normal'), (b'M', b'Mad'), (b'A', b'Angry')])),
                ('parent', models.ForeignKey(blank=True, to='game.Dialogue', null=True)),
            ],
            options={
                'verbose_name': 'dialogue',
                'verbose_name_plural': 'dialogues',
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('background', models.ImageField(upload_to=b'images/', verbose_name='background image')),
                ('role', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'scenario',
                'verbose_name_plural': 'scenarios',
            },
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context', models.TextField(null=True, verbose_name='context', blank=True)),
                ('scene', models.TextField(null=True, verbose_name='scene', blank=True)),
                ('scenario', models.ForeignKey(to='game.Scenario')),
            ],
            options={
                'verbose_name': 'script',
                'verbose_name_plural': 'scripts',
            },
        ),
        migrations.AddField(
            model_name='dialogue',
            name='script',
            field=models.ForeignKey(to='game.Script'),
        ),
        migrations.AddField(
            model_name='character',
            name='scenario',
            field=models.ForeignKey(to='game.Scenario'),
        ),
    ]
