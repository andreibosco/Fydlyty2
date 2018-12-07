# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Fydlyty2.game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20150707_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctfile',
            name='ct_script',
            field=models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='ctfile',
            name='script',
            field=models.ForeignKey(to='game.Script'),
        ),
    ]
