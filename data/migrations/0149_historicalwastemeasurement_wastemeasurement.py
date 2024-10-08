# Generated by Django 5.1 on 2024-08-28 10:32

import data.models.wastemeasurement
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0148_alter_canteen_line_ministry_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalWasteMeasurement",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("creation_date", models.DateTimeField(blank=True, editable=False)),
                ("modification_date", models.DateTimeField(blank=True, editable=False)),
                ("period_start_date", models.DateField(verbose_name="date de début")),
                (
                    "period_end_date",
                    models.DateField(
                        validators=[data.models.wastemeasurement.validate_before_today],
                        verbose_name="date de fin",
                    ),
                ),
                (
                    "meal_count",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="couverts sur la période"
                    ),
                ),
                (
                    "total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="Masse totale",
                    ),
                ),
                (
                    "is_sorted_by_source",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="trié en fonctionne de source ?",
                    ),
                ),
                (
                    "preparation_total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="préparation - masse totale",
                    ),
                ),
                (
                    "preparation_is_sorted",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="préparation - trié en fonction de comestible/non-comestible ?",
                    ),
                ),
                (
                    "preparation_edible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="préparation - masse comestible",
                    ),
                ),
                (
                    "preparation_inedible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="préparation - masse non-comestible",
                    ),
                ),
                (
                    "unserved_total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="non-servi - masse totale",
                    ),
                ),
                (
                    "unserved_is_sorted",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="non-servi - trié en fonction de comestible/non-comestible ?",
                    ),
                ),
                (
                    "unserved_edible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="non-servi - masse comestible",
                    ),
                ),
                (
                    "unserved_inedible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="non-servi - masse non-comestible",
                    ),
                ),
                (
                    "leftovers_total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="restes assiette - masse totale",
                    ),
                ),
                (
                    "leftovers_is_sorted",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="restes assiette - trié en fonction de comestible/non-comestible ?",
                    ),
                ),
                (
                    "leftovers_edible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="restes assiette - masse comestible",
                    ),
                ),
                (
                    "leftovers_inedible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="restes assiette - masse non-comestible",
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "canteen",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="data.canteen",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical pesage du gaspillage alimentaire",
                "verbose_name_plural": "historical pesages du gaspillage alimentaire",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="WasteMeasurement",
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
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("modification_date", models.DateTimeField(auto_now=True)),
                ("period_start_date", models.DateField(verbose_name="date de début")),
                (
                    "period_end_date",
                    models.DateField(
                        validators=[data.models.wastemeasurement.validate_before_today],
                        verbose_name="date de fin",
                    ),
                ),
                (
                    "meal_count",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="couverts sur la période"
                    ),
                ),
                (
                    "total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="Masse totale",
                    ),
                ),
                (
                    "is_sorted_by_source",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="trié en fonctionne de source ?",
                    ),
                ),
                (
                    "preparation_total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="préparation - masse totale",
                    ),
                ),
                (
                    "preparation_is_sorted",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="préparation - trié en fonction de comestible/non-comestible ?",
                    ),
                ),
                (
                    "preparation_edible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="préparation - masse comestible",
                    ),
                ),
                (
                    "preparation_inedible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="préparation - masse non-comestible",
                    ),
                ),
                (
                    "unserved_total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="non-servi - masse totale",
                    ),
                ),
                (
                    "unserved_is_sorted",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="non-servi - trié en fonction de comestible/non-comestible ?",
                    ),
                ),
                (
                    "unserved_edible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="non-servi - masse comestible",
                    ),
                ),
                (
                    "unserved_inedible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="non-servi - masse non-comestible",
                    ),
                ),
                (
                    "leftovers_total_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="restes assiette - masse totale",
                    ),
                ),
                (
                    "leftovers_is_sorted",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="restes assiette - trié en fonction de comestible/non-comestible ?",
                    ),
                ),
                (
                    "leftovers_edible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="restes assiette - masse comestible",
                    ),
                ),
                (
                    "leftovers_inedible_mass",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="restes assiette - masse non-comestible",
                    ),
                ),
                (
                    "canteen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="data.canteen"
                    ),
                ),
            ],
            options={
                "verbose_name": "pesage du gaspillage alimentaire",
                "verbose_name_plural": "pesages du gaspillage alimentaire",
            },
        ),
    ]
