# Generated by Django 3.2.3 on 2021-06-09 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_rename_comunicates_on_food_plan_diagnostic_communicates_on_food_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='has_waste_diagnostic',
            field=models.BooleanField(null=True, verbose_name='diagnostic sur le gaspillage réalisé'),
        ),
    ]
