# Generated by Django 5.0 on 2023-12-27 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]