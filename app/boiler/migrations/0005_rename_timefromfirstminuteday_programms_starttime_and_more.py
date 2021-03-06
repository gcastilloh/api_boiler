# Generated by Django 4.0.5 on 2022-06-13 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boiler', '0004_programms_timefromfirstminuteday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programms',
            old_name='timeFromFirstMinuteDay',
            new_name='startTime',
        ),
        migrations.AddField(
            model_name='programms',
            name='endTime',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2880)]),
            preserve_default=False,
        ),
    ]
