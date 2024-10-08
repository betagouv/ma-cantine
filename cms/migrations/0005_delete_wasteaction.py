# Generated by Django 5.0.7 on 2024-09-09 16:22

from django.db import migrations
from django.core.serializers import serialize


def backup_waste_action_data(apps, schema_editor):
    try:
        WasteAction = apps.get_model("cms", "WasteAction")
        data = serialize("json", WasteAction.objects.all())
        with open("waste_action_backup.json", "w") as f:
            f.write(data)
    except:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0004_alter_wasteaction_subtitle"),
    ]

    operations = [
        migrations.RunPython(backup_waste_action_data),
        migrations.DeleteModel(
            name="WasteAction",
        ),
    ]
