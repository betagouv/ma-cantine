from django.db import migrations, models

NEW_FIELDS = [
    (
        "information_affichage_permanent",
        "La cantine dispose d’un affichage permanent à l’entrée du restaurant, actualisé au moins une fois par an et lisible par tous les usagers",
    ),
    (
        "information_electronique_annuelle",
        "Une communication électronique (réalisée au moins une fois par an) permet aux usagers d’être informés",
    ),
    (
        "information_part_egalim",
        "Part de produits EGalim (dont bio) entrant dans la composition des repas servis",
    ),
    (
        "information_part_pat",
        "Part des produits issus de Projets alimentaires territoriaux (PAT)",
    ),
    (
        "information_consultation_qualite",
        "L’établissement informe et consulte régulièrement, par tous moyens utiles, les usagers sur le respect de la qualité alimentaire et nutritionnelle des repas servis",
    ),
]


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0300_diagnostic_plastique_french_field_names"),
    ]

    operations = [
        migrations.AddField(
            model_name=model_name,
            name=field_name,
            field=models.BooleanField(blank=True, null=True, verbose_name=verbose_name),
        )
        for model_name in ["diagnostic", "historicaldiagnostic"]
        for field_name, verbose_name in NEW_FIELDS
    ]
