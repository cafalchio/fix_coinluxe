# Generated by Django 3.2.19 on 2023-06-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_backend", "0014_auto_20230615_0155"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cryptocurrency",
            name="id",
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="cryptocurrency",
            name="name",
            field=models.CharField(max_length=200),
        ),
    ]
