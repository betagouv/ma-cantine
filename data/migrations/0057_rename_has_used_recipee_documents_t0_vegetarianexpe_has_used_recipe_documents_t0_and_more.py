# Generated by Django 4.0.3 on 2022-04-05 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0056_canteen_vegetarian_expe_participant_vegetarianexpe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vegetarianexpe',
            old_name='has_used_recipee_documents_t0',
            new_name='has_used_recipe_documents_t0',
        ),
        migrations.RenameField(
            model_name='vegetarianexpe',
            old_name='has_used_recipee_documents_t1',
            new_name='has_used_recipe_documents_t1',
        ),
    ]
