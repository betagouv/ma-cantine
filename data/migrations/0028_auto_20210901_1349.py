# Generated by Django 3.2.6 on 2021-09-01 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0027_merge_20210831_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teledeclaration',
            old_name='fields',
            new_name='declared_data',
        ),
        migrations.AlterField(
            model_name='teledeclaration',
            name='applicant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='déclarant'),
        ),
    ]
