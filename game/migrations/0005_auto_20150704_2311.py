# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20150612_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='gender',
            field=models.CharField(default=b'', max_length=2, choices=[(b'', b''), (b'M', b'Male'), (b'F', b'Female'), (b'N', b"I don't want to say")]),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='background',
            field=models.ImageField(upload_to=b'BackgroundImages/', verbose_name='background image'),
        ),
    ]
