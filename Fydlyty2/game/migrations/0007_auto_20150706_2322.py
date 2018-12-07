# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_scenario_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ctfile',
            name='dialogue',
        ),
        migrations.RemoveField(
            model_name='ctfile',
            name='scenario',
        ),
        migrations.AddField(
            model_name='ctfile',
            name='mood',
            field=models.CharField(default=b'N', max_length=2, null=True, blank=True, choices=[(b'N', b'Normal'), (b'M', b'Mad'), (b'A', b'Angry')]),
        ),
        migrations.AddField(
            model_name='ctfile',
            name='script',
            field=models.ForeignKey(default=105, to='game.Script'),
            preserve_default=False,
        ),
    ]
