# Generated by Django 4.2.4 on 2023-08-17 21:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0124_user_departments_user_is_elected"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_elected",
            new_name="is_elected_official",
        ),
    ]
