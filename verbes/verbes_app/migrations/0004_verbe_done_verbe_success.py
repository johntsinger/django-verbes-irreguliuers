# Generated by Django 4.0.4 on 2022-05-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verbes_app', '0003_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='verbe',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verbe',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]