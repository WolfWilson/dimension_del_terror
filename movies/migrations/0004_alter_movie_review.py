# Generated by Django 5.1.3 on 2024-12-16 11:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_header_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='review',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]