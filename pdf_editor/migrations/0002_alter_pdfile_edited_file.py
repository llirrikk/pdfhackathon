# Generated by Django 3.2.8 on 2021-10-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfile',
            name='edited_file',
            field=models.FileField(blank=True, upload_to='media/'),
        ),
    ]
