# Generated by Django 4.0.5 on 2022-06-10 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boiler', '0002_programms_unico'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programms',
            old_name='unico',
            new_name='unic',
        ),
    ]