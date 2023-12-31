# Generated by Django 3.2.19 on 2023-06-13 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_backend", "0007_auto_20230613_2234"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coins",
            name="block_time_in_minutes",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="coins",
            name="blockchain_site",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="coins",
            name="categories",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="coins",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="coins",
            name="homepage",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
