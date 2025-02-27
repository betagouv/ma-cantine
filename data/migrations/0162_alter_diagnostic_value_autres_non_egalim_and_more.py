# Generated by Django 5.0.7 on 2025-01-10 17:53

import data.fields
import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0161_alter_canteen_daily_meal_count_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diagnostic",
            name="value_autres_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Autres produits frais, surgelés et d’épicerie, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_boissons_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Boissons, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_boulangerie_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Boulangerie/Pâtisserie fraîches, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_charcuterie_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Charcuterie, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_egalim_others_ht",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Valeur totale (HT) des autres achats EGalim",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_fish_egalim_ht",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Valeur totale (HT) poissons et produits aquatiques EGalim",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_fruits_et_legumes_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Fruits et légumes frais et surgelés, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_meat_poultry_egalim_ht",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_produits_de_la_mer_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Produits aquatiques frais et surgelés, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_produits_laitiers_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="BOF (Produits laitiers, beurre et œufs), non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="diagnostic",
            name="value_viandes_volailles_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Viandes et volailles fraîches et surgelées, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_autres_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Autres produits frais, surgelés et d’épicerie, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_boissons_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Boissons, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_boulangerie_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Boulangerie/Pâtisserie fraîches, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_charcuterie_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Charcuterie, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_egalim_others_ht",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Valeur totale (HT) des autres achats EGalim",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_fish_egalim_ht",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Valeur totale (HT) poissons et produits aquatiques EGalim",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_fruits_et_legumes_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Fruits et légumes frais et surgelés, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_meat_poultry_egalim_ht",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_produits_de_la_mer_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Produits aquatiques frais et surgelés, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_produits_laitiers_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="BOF (Produits laitiers, beurre et œufs), non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnostic",
            name="value_viandes_volailles_non_egalim",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=20,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Viandes et volailles fraîches et surgelées, non-EGalim.",
            ),
        ),
        migrations.AlterField(
            model_name="historicalteledeclaration",
            name="teledeclaration_mode",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "SATELLITE_WITHOUT_APPRO",
                        "Cantine satellite dont les données d'appro sont déclarées par la cuisine centrale",
                    ),
                    (
                        "CENTRAL_APPRO",
                        "Cuisine centrale déclarant les données d'appro pour ses cuisines satellites",
                    ),
                    (
                        "CENTRAL_ALL",
                        "Cuisine centrale déclarant toutes les données EGalim pour ses cuisines satellites",
                    ),
                    ("SITE", "Cantine déclarant ses propres données"),
                ],
                max_length=255,
                null=True,
                verbose_name="mode de télédéclaration",
            ),
        ),
        migrations.AlterField(
            model_name="teledeclaration",
            name="teledeclaration_mode",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "SATELLITE_WITHOUT_APPRO",
                        "Cantine satellite dont les données d'appro sont déclarées par la cuisine centrale",
                    ),
                    (
                        "CENTRAL_APPRO",
                        "Cuisine centrale déclarant les données d'appro pour ses cuisines satellites",
                    ),
                    (
                        "CENTRAL_ALL",
                        "Cuisine centrale déclarant toutes les données EGalim pour ses cuisines satellites",
                    ),
                    ("SITE", "Cantine déclarant ses propres données"),
                ],
                max_length=255,
                null=True,
                verbose_name="mode de télédéclaration",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="law_awareness",
            field=data.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        (
                            "NONE",
                            "Je n’ai pas une connaissance détaillée de l’article 24 de la loi EGalim",
                        ),
                        ("AIMS_DEADLINES", "Je connais les objectifs et les échéances"),
                        (
                            "ELIGIBLE_LABELS",
                            "Je connais la liste des labels éligibles et mentions valorisantes",
                        ),
                        (
                            "MY_LABELS",
                            "J’ai accès aux informations ou mon prestataire me fournit les informations sur les labels éligibles et mentions valorisantes concernant mes achats",
                        ),
                        (
                            "SYSTEM",
                            "J’ai un système de saisie formalisé (SI, Excel, papier) permettant de calculer et reporter le montant annuel de mes achats répondants aux exigences de l’article 24 de la loi EGalim (Non applicable en gestion concédée)",
                        ),
                        (
                            "TAKEN_STOCK",
                            "J’ai réalisé un état des lieux précis de mes approvisionnements",
                        ),
                        (
                            "OPTION_DIAGNOSTIC",
                            "J’ai réalisé un diagnostic de l’offre (disponibilité et caractéristiques de l’offre des différents fournisseurs sur l’ensemble des catégories d’achats)",
                        ),
                        (
                            "ACTION_PLAN",
                            "J’ai établi un plan d’actions pour tendre vers les objectifs de la loi EGalim, définissant notamment : le niveau d’ambition global et par catégories d’achats ; les échéances de renouvellement de contrat avec clauses EGalim ; le phasage de la progression des indicateurs EGalim",
                        ),
                        (
                            "QUALITY_ACHIEVED",
                            "J'ai atteint les objectifs - 50% et 20%, de l’article 24 de la loi EGalim",
                        ),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="Les affirmations suivantes concernent l'article 24 de la loi EGalim, encadrant les objectifs d'approvisionnements (50% de produits durables et de qualité dont 20% de bio). Parmi ces affirmations, plusieurs choix sont possibles. Choisissez celles qui correspondent à votre situation :",
            ),
        ),
    ]
