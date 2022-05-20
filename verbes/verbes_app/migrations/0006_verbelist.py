# Generated by Django 4.0.4 on 2022-05-18 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verbes_app', '0005_table_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerbeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='verbes_app.table')),
                ('verbe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='verbes_app.verbe')),
            ],
        ),
    ]
