# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20150610_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='gender',
            field=models.CharField(default=b'', max_length=2, choices=[(b'', b''), (b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AddField(
            model_name='character',
            name='marital_status',
            field=models.CharField(default=b'', max_length=2, choices=[(b'N', b"I don't want to say"), (b'S', b'Single'), (b'R', b'In a relationship'), (b'E', b'Engaged'), (b'M', b'Married'), (b'W', b'Widowed'), (b'SP', b'Seperated'), (b'D', b'Divorced')]),
        ),
        migrations.AddField(
            model_name='character',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
