# Generated by Django 3.2.19 on 2023-05-23 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cryptocurrency',
            name='roi',
        ),
    ]
