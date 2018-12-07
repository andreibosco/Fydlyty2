# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Fydlyty2.game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20150706_2322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ctfile',
            old_name='file1',
            new_name='idle',
        ),
        migrations.RenameField(
            model_name='ctfile',
            old_name='file2',
            new_name='model',
        ),
        migrations.RenameField(
            model_name='ctfile',
            old_name='file3',
            new_name='motion',
        ),
        migrations.RenameField(
            model_name='ctfile',
            old_name='file4',
            new_name='project',
        ),
        migrations.RemoveField(
            model_name='ctfile',
            name='file5',
        ),
        migrations.AlterField(
            model_name='ctfile',
            name='script',
            field=models.FileField(upload_to=Fydlyty2.game.models.get_upload_path, blank=True),
        ),
    ]
