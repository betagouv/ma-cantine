# Generated by Django 3.2.6 on 2021-09-13 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0030_alter_diversification_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='value_pat_ht',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Produits dans le cadre de Projects Alimentaires Territoriaux - Valeur annuelle HT'),
        ),
    ]
