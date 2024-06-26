# Generated by Django 3.2.3 on 2021-06-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_squashed_0006_blogpost_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='canteen',
            name='management_type',
            field=models.CharField(blank=True, choices=[('direct', 'Directe'), ('conceded', 'Concédée')], max_length=255, null=True, verbose_name='mode de gestion'),
        ),
        migrations.AddField(
            model_name='canteen',
            name='siret',
            field=models.TextField(blank=True, null=True),
        ),
    ]
