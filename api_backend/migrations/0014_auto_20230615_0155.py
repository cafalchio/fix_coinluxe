# Generated by Django 3.2.19 on 2023-06-15 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_backend", "0013_rename_coin_priceupdate_coin_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="priceupdate",
            name="coin_id",
        ),
        migrations.AlterField(
            model_name="priceupdate",
            name="id",
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
