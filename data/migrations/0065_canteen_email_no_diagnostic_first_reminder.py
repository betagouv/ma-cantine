# Generated by Django 4.0.4 on 2022-05-06 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0064_canteen_creation_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='canteen',
            name='email_no_diagnostic_first_reminder',
            field=models.DateTimeField(blank=True, null=True, verbose_name="Date d'envoi du premier email pour manque de diagnostics"),
        ),
    ]
