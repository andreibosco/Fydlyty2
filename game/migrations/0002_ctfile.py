# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Fydlyty2.game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CTFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file1', models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True)),
                ('dialogue', models.ForeignKey(to='game.Dialogue')),
                ('scenario', models.ForeignKey(to='game.Scenario')),
            ],
            options={
                'verbose_name': 'crazy talk file',
                'verbose_name_plural': 'crazy talk files',
            },
        ),
    ]
