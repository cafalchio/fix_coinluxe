# Generated by Django 3.2.19 on 2023-05-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_backend", "0003_auto_20230523_2055"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cryptocurrency",
            name="price_change_24h",
            field=models.FloatField(null=True),
        ),
    ]
