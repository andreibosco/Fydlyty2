# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20150704_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='type',
            field=models.CharField(default=b'B', max_length=2, choices=[(b'B', b'Basic Scenario'), (b'C', b'Complex Scenario')]),
        ),
    ]
