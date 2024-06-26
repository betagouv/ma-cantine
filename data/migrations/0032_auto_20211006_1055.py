# Generated by Django 3.2.7 on 2021-10-06 08:55

from django.db import migrations, models
import django.db.models.deletion


def migrate_images(apps, schema_editor):
    """
    If a cantine had already an image uploaded to the "logo" field,
    we will move it to a CanteenImage model.
    """
    Canteen = apps.get_model("data", "Canteen")
    CanteenImage = apps.get_model("data", "CanteenImage")
    for canteen in Canteen.objects.all():
        if canteen.logo:
            image = CanteenImage(canteen=canteen, image=canteen.logo)
            image.save()
            canteen.logo = None
            canteen.save()


def undo_migrate_images(apps, schema_editor):
    """
    If a cantine has a CanteenImage model linked to it, we will
    put the first image as the "logo"
    """
    Canteen = apps.get_model("data", "Canteen")
    for canteen in Canteen.objects.all():
        if canteen.images.count() > 0:
            canteen.logo = canteen.images.first().image
            canteen.save()


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0031_diagnostic_add_pat_value"),
    ]

    operations = [
        migrations.RenameField(
            model_name="canteen", old_name="main_image", new_name="logo"
        ),
        migrations.AlterField(
            model_name="canteen",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Logo"
            ),
        ),
        migrations.CreateModel(
            name="CanteenImage",
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
                ("image", models.ImageField(upload_to="")),
                (
                    "canteen",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="data.canteen",
                    ),
                ),
            ],
        ),
        migrations.RunPython(migrate_images, undo_migrate_images),
    ]
