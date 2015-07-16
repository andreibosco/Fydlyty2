# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Fydlyty2.game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20150708_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctfile',
            name='ct_script',
            field=models.FileField(max_length=500, upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='ctfile',
            name='idle',
            field=models.FileField(max_length=500, upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='ctfile',
            name='model',
            field=models.FileField(max_length=500, upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='ctfile',
            name='motion',
            field=models.FileField(max_length=500, upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='ctfile',
            name='project',
            field=models.FileField(max_length=500, upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
    ]
