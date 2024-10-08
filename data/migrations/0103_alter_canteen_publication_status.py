# Generated by Django 4.1.3 on 2023-02-21 13:24

from django.db import migrations, models


def validate_pending_publications(apps, schema_editor):
    Canteen = apps.get_model("data", "Canteen")
    # Here we don't have access to Canteen.PublicationStatus TextChoices
    for canteen in Canteen.objects.filter(publication_status="pending"):
        canteen.publication_status = "published"
        canteen.save()


def undo_validate_pending_publications(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0102_alter_canteen_economic_model"),
    ]

    operations = [
        migrations.RunPython(validate_pending_publications, undo_validate_pending_publications),
        migrations.AlterField(
            model_name="canteen",
            name="publication_status",
            field=models.CharField(
                choices=[("draft", "🔒 Non publié"), ("published", "✅ Publié")],
                default="draft",
                max_length=50,
                verbose_name="état de publication",
            ),
        ),
    ]
