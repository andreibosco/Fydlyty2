# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Fydlyty2.game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_ctfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctfile',
            name='file2',
            field=models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AddField(
            model_name='ctfile',
            name='file3',
            field=models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AddField(
            model_name='ctfile',
            name='file4',
            field=models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AddField(
            model_name='ctfile',
            name='file5',
            field=models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='background',
            field=models.ImageField(upload_to=b'Fydlyty2/media/BackgroundImages/', verbose_name='background image'),
        ),
    ]
