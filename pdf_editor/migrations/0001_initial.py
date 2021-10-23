# Generated by Django 3.2.8 on 2021-10-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PDFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='media/')),
                ('edited_file', models.FileField(upload_to='media/')),
                ('upload_time', models.DateTimeField(blank=True)),
                ('download_counter', models.PositiveIntegerField(blank=True)),
                ('user_ip', models.GenericIPAddressField()),
            ],
        ),
    ]
