# Generated by Django 5.0 on 2024-01-02 14:17

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageapp', '0008_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]