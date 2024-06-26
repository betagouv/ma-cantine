# Generated by Django 4.0.3 on 2022-04-14 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0060_merge_20220414_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canteen',
            name='line_ministry',
            field=models.TextField(blank=True, choices=[('premier_ministre', 'Service du Premier Ministre'), ('affaires_etrangeres', 'Ministère de l’Europe et des Affaires étrangères'), ('ecologie', 'Ministère de la Transition écologique'), ('jeunesse', 'Ministère de l’Education Nationale et de la Jeunesse et des Sports'), ('economie', 'Ministère de l’Economie, de la Finance et de la Relance'), ('armee', 'Ministère de l’Armée'), ('interieur', 'Ministère de l’Intérieur'), ('travail', 'Ministère Travail, de l’Emploi et de l’Insertion'), ('outre_mer', 'Ministère des Outre-mer'), ('territoires', 'Ministère de la Cohésion des Territoires et des Relations avec les Collectivités Territoriales'), ('justice', 'Ministère de la Justice'), ('culture', 'Ministère de la Culture'), ('sante', 'Ministère des Solidarités et de la Santé'), ('mer', 'Ministère de la Mer'), ('enseignement_superieur', 'Ministère de l’Enseignement Supérieur et de la Recherche et de l’Innovation'), ('agriculture', 'Ministère de l’Agriculture et de l’Alimentation'), ('transformation', 'Ministère de la Transformation et de la Fonction Publiques'), ('autre', 'Autre')], null=True, verbose_name='Ministère de tutelle'),
        ),
    ]
