# Generated by Django 5.1.7 on 2025-03-21 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("global_neighbor", "0005_alter_user_verification_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="verification_token",
            field=models.CharField(max_length=64),
        ),
    ]
