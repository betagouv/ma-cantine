# Generated by Django 3.2.11 on 2022-01-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0041_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='price_ht',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Prix HT'),
            preserve_default=False,
        ),
    ]
