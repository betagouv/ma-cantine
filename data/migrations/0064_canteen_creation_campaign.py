# Generated by Django 4.0.4 on 2022-04-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0063_merge_0062_merge_20220414_1128_0062_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='canteen',
            name='creation_campaign',
            field=models.TextField(blank=True, null=True, verbose_name='Campagne à la source de la création'),
        ),
    ]
