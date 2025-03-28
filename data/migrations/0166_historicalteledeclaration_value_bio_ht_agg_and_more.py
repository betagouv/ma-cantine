# Generated by Django 5.0.13 on 2025-03-26 09:16

from django.db import migrations, models
        
class Migration(migrations.Migration):


    dependencies = [
        ("data", "0165_historicalteledeclaration_canteen_siren_unite_legale_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalteledeclaration",
            name="value_bio_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ value bio. En cas de TD complète: ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="historicalteledeclaration",
            name="value_egalim_others_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ Autres Egalim. En cas de TD complète, ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="historicalteledeclaration",
            name="value_externality_performance_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ externalité/performance. En cas de TD complète, ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="historicalteledeclaration",
            name="value_sustainable_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ value Egalim. En cas de TD complète: ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="historicalteledeclaration",
            name="value_total_ht",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ value total. En cas de TD complète: ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="teledeclaration",
            name="value_bio_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ value bio. En cas de TD complète: ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="teledeclaration",
            name="value_egalim_others_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ Autres Egalim. En cas de TD complète, ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="teledeclaration",
            name="value_externality_performance_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ externalité/performance. En cas de TD complète, ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="teledeclaration",
            name="value_sustainable_ht_agg",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ value Egalim. En cas de TD complète: ce champ est aggrégé",
            ),
        ),
        migrations.AddField(
            model_name="teledeclaration",
            name="value_total_ht",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Champ value total. En cas de TD complète: ce champ est aggrégé",
            ),
        ),
    ]
