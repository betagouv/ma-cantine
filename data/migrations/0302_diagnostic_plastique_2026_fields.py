from django.db import migrations, models

NEW_FIELDS = [
    (
        "plastique_bouteille_boisson_remplace",
        "La cantine est équipée d’au moins une fontaine d'eau potable accessible au public et n’assure aucune distribution gratuite de bouteilles en plastique contenant des boissons",
    ),
    (
        "plastique_vaisselle_jetable_remplace",
        "Aucune vaisselle jetable n’est utilisée pour les repas consommés sur place (gobelets, assiette et récipients, couverts)",
    ),
    (
        "plastique_contenant_remplace",
        "Aucun contenant alimentaire de cuisson, de réchauffage et de service en plastique sont utilisés au sein de l’établissement",
    ),
    (
        "plastique_contenant_emporter_remplace",
        "Des contenants réutilisables ou composés de matières recyclables sont proposés pour l’ensemble des repas à emporter",
    ),
]


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0301_diagnostic_information_2026_fields"),
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
