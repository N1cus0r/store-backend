# Generated by Django 4.1.5 on 2023-01-10 16:28

from django.db import migrations, models
import productsapi.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand", models.CharField(max_length=50)),
                ("model", models.CharField(max_length=100)),
                ("category", models.CharField(max_length=50)),
                ("subcategory", models.CharField(max_length=50)),
                ("sex", models.CharField(max_length=5)),
                ("price", models.IntegerField()),
                (
                    "image",
                    models.ImageField(upload_to=productsapi.models.get_upload_path),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
    ]
