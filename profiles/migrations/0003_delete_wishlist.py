# Generated by Django 3.2.22 on 2023-12-09 20:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_wishlist"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Wishlist",
        ),
    ]
