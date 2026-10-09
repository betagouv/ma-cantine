from rest_framework import serializers

from api.serializers.utils import ReadOnlySerializerMixin
from data.models import Canteen, Diagnostic
from data.models.geo import Department, Region
from macantine.etl import utils


class DiagnosticTeledeclaredAnalysisSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(source="teledeclaration_id")
    creation_date = serializers.DateTimeField(source="teledeclaration_date")
    version = serializers.CharField(source="teledeclaration_version")

    canteen_id = serializers.IntegerField(source="canteen_snapshot.id")
    name = serializers.CharField(source="canteen_snapshot.name")
    siret = serializers.CharField(source="canteen_snapshot.siret")
    siren_unite_legale = serializers.CharField(source="canteen_snapshot.siren_unite_legale")
    daily_meal_count = serializers.IntegerField(source="canteen_snapshot.daily_meal_count")
    yearly_meal_count = serializers.IntegerField(source="canteen_snapshot.yearly_meal_count")
    cout_denrees = serializers.FloatField(source="cout_repas")
    cuisine_centrale = serializers.SerializerMethodField()
    central_producer_siret = serializers.CharField(source="canteen_snapshot.central_producer_siret")
    code_insee_commune = serializers.CharField(source="canteen_snapshot.city_insee_code")
    epci = serializers.CharField(source="canteen_snapshot.epci")
    # epci_lib = serializers.CharField(source="canteen_snapshot.epci_lib", read_only=True)
    pat_list = serializers.SerializerMethodField()
    # pat_lib_list = serializers.ListField(source="canteen_snapshot.pat_lib_list", read_only=True)
    departement = serializers.CharField(source="canteen_snapshot.department")
    lib_departement = (
        serializers.SerializerMethodField()
    )  # serializers.CharField(source="canteen_snapshot.department_lib")
    region = serializers.CharField(source="canteen_snapshot.region")
    lib_region = serializers.SerializerMethodField()  # serializers.CharField(source="canteen_snapshot.region_lib")
    nbre_cantines_region = serializers.SerializerMethodField()
    objectif_zone_geo = serializers.SerializerMethodField()
    secteur = serializers.SerializerMethodField()
    categorie = serializers.SerializerMethodField()
    line_ministry = serializers.CharField(source="canteen_snapshot.line_ministry")
    spe = serializers.SerializerMethodField()
    modele_economique = serializers.CharField(source="canteen_snapshot.economic_model")
    management_type = serializers.CharField(source="canteen_snapshot.management_type")
    production_type = serializers.CharField(source="canteen_snapshot.production_type")
    is_filled = serializers.BooleanField(source="canteen_snapshot.is_filled")
    declaration_donnees_2021 = serializers.SerializerMethodField()
    declaration_donnees_2022 = serializers.SerializerMethodField()
    declaration_donnees_2023 = serializers.SerializerMethodField()
    declaration_donnees_2024 = serializers.SerializerMethodField()
    declaration_donnees_2025 = serializers.SerializerMethodField()
    # TODO teledeclaration_campaign: add new year

    valeur_bio = serializers.FloatField(source="valeur_bio_agg")
    valeur_siqo = serializers.FloatField(source="valeur_siqo_agg")
    valeur_externalites_performance = serializers.FloatField(source="valeur_externalites_performance_agg")
    valeur_egalim_autres = serializers.FloatField(source="valeur_egalim_autres_agg")
    valeur_somme_egalim_avec_bio = serializers.FloatField(source="valeur_egalim_agg")
    valeur_somme_egalim_hors_bio = serializers.SerializerMethodField()
    valeur_viandes_volailles_produits_de_la_mer = serializers.SerializerMethodField()
    valeur_viandes_volailles_produits_de_la_mer_egalim = serializers.SerializerMethodField()
    ratio_produits_de_la_mer_egalim = serializers.SerializerMethodField()
    ratio_viandes_volailles_egalim = serializers.SerializerMethodField()
    ratio_bio = serializers.SerializerMethodField()
    ratio_egalim_avec_bio = serializers.SerializerMethodField()
    ratio_egalim_sans_bio = serializers.SerializerMethodField()
    diag_gaspi = serializers.BooleanField(source="has_waste_diagnostic")
    plan_action_gaspi = serializers.BooleanField(source="has_waste_plan")
    action_gaspi_inscription = serializers.SerializerMethodField()
    action_gaspi_sensibilisation = serializers.SerializerMethodField()
    action_gaspi_formation = serializers.SerializerMethodField()
    action_gaspi_distribution = serializers.SerializerMethodField()
    action_gaspi_portions = serializers.SerializerMethodField()
    action_gaspi_reutilisation = serializers.SerializerMethodField()

    email = serializers.EmailField(source="applicant_snapshot.email")
    tmp_satellites = serializers.ListField(source="satellites_snapshot")
    genere_par_cuisine_centrale = serializers.SerializerMethodField()

    class Meta:
        model = Diagnostic
        fields = (
            # diagnostic fields
            "id",  # teledeclaration_id
            "diagnostic_type",
            "teledeclaration_mode",
            "creation_date",  # teledeclaration_date
            "year",
            "version",
            "creation_source",
            # applicant fields
            "email",
            # canteen fields
            "canteen_id",
            "name",
            "siret",
            "siren_unite_legale",
            "daily_meal_count",
            "yearly_meal_count",
            "cout_denrees",
            "cuisine_centrale",
            "central_producer_siret",
            "code_insee_commune",
            "epci",
            # "epci_lib",
            "pat_list",
            # "pat_lib_list",
            "departement",
            "lib_departement",
            "region",
            "lib_region",
            "nbre_cantines_region",
            "objectif_zone_geo",
            "secteur",
            "categorie",
            "line_ministry",
            "spe",
            "modele_economique",
            "management_type",
            "production_type",
            "is_filled",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
            "declaration_donnees_2025",
            # value fields
            "valeur_totale",
            "valeur_bio",
            "valeur_siqo",
            "valeur_externalites_performance",
            "valeur_egalim_autres",
            "valeur_viandes_volailles",
            "valeur_viandes_volailles_france",
            "valeur_viandes_volailles_egalim",
            "valeur_produits_de_la_mer",
            "valeur_produits_de_la_mer_egalim",
            "valeur_somme_egalim_avec_bio",
            "valeur_somme_egalim_hors_bio",
            "valeur_viandes_volailles_produits_de_la_mer",
            "valeur_viandes_volailles_produits_de_la_mer_egalim",
            "service_type",
            "vegetarian_weekly_recurrence",
            "vegetarian_menu_type",
            "diag_gaspi",
            "plan_action_gaspi",
            "action_gaspi_inscription",
            "action_gaspi_sensibilisation",
            "action_gaspi_formation",
            "action_gaspi_distribution",
            "action_gaspi_portions",
            "action_gaspi_reutilisation",
            "ratio_produits_de_la_mer_egalim",
            "ratio_viandes_volailles_egalim",
            "ratio_bio",
            "ratio_egalim_avec_bio",
            "ratio_egalim_sans_bio",
            # extra
            "tmp_satellites",
            "genere_par_cuisine_centrale",
        )

    def get_cuisine_centrale(self, obj):
        production_type = obj.canteen_snapshot.get("production_type", None)
        if production_type in ["site", "site_cooked_elsewhere"]:
            return "B) non"
        elif production_type in ["central", "central_serving"]:
            return "A) oui"
        else:
            return "C) non renseigné"

    def get_secteur(self, obj):
        return ",".join(obj.canteen_snapshot_sector_lib_list or [])

    def get_categorie(self, obj):
        return ",".join(obj.canteen.category_lib_list_from_sector_list or [])

    def get_pat_list(self, obj):
        return ",".join(obj.canteen_snapshot.get("pat_list", []) or [])

    def get_lib_departement(self, obj):
        department = obj.canteen_snapshot.get("department", None)
        return Department(department).label.split(" - ")[1].lstrip() if department else None

    def get_lib_region(self, obj):
        region = obj.canteen_snapshot.get("region", None)
        return Region(region).label.split(" - ")[1].lstrip() if region else None

    def get_nbre_cantines_region(self, obj):
        return utils.get_nbre_cantines_region(obj.canteen_snapshot.get("region", None))

    def get_objectif_zone_geo(self, obj):
        return utils.get_objectif_zone_geo(obj.canteen_snapshot.get("department", None))

    def get_spe(self, obj):
        line_ministry = obj.canteen_snapshot.get("line_ministry", None)
        return "Oui" if line_ministry else "Non"

    def get_declaration_donnees_2021(self, obj):
        return obj.canteen.declaration_donnees_2021

    def get_declaration_donnees_2022(self, obj):
        return obj.canteen.declaration_donnees_2022

    def get_declaration_donnees_2023(self, obj):
        return obj.canteen.declaration_donnees_2023

    def get_declaration_donnees_2024(self, obj):
        return obj.canteen.declaration_donnees_2024

    def get_declaration_donnees_2025(self, obj):
        return obj.canteen.declaration_donnees_2025

    def get_valeur_somme_egalim_hors_bio(self, obj):
        return utils.sum_int_and_none(
            [
                obj.valeur_siqo_agg,
                obj.valeur_externalites_performance_agg,
                obj.valeur_egalim_autres_agg,
            ]
        )

    def get_valeur_viandes_volailles_produits_de_la_mer(self, obj):
        return utils.sum_int_and_none([obj.valeur_viandes_volailles, obj.valeur_produits_de_la_mer])

    def get_valeur_viandes_volailles_produits_de_la_mer_egalim(self, obj):
        return utils.sum_int_and_none([obj.valeur_viandes_volailles_egalim, obj.valeur_produits_de_la_mer_egalim])

    def get_action_gaspi_inscription(self, obj):
        return obj.waste_actions and (Diagnostic.WasteActions.INSCRIPTION in obj.waste_actions)

    def get_action_gaspi_sensibilisation(self, obj):
        return obj.waste_actions and (Diagnostic.WasteActions.AWARENESS in obj.waste_actions)

    def get_action_gaspi_formation(self, obj):
        return obj.waste_actions and (Diagnostic.WasteActions.TRAINING in obj.waste_actions)

    def get_action_gaspi_distribution(self, obj):
        return obj.waste_actions and (Diagnostic.WasteActions.DISTRIBUTION in obj.waste_actions)

    def get_action_gaspi_portions(self, obj):
        return obj.waste_actions and (Diagnostic.WasteActions.PORTIONS in obj.waste_actions)

    def get_action_gaspi_reutilisation(self, obj):
        return obj.waste_actions and (Diagnostic.WasteActions.REUSE in obj.waste_actions)

    def get_ratio_produits_de_la_mer_egalim(self, obj):
        return utils.compute_percentage(obj.valeur_produits_de_la_mer_egalim, obj.valeur_produits_de_la_mer)

    def get_ratio_viandes_volailles_egalim(self, obj):
        return utils.compute_percentage(obj.valeur_viandes_volailles_egalim, obj.valeur_viandes_volailles)

    def get_ratio_bio(self, obj):
        if obj.pourcentage_bio:
            return obj.pourcentage_bio

    def get_ratio_egalim_avec_bio(self, obj):
        if obj.pourcentage_egalim:
            return obj.pourcentage_egalim

    def get_ratio_egalim_sans_bio(self, obj):
        if obj.pourcentage_egalim_hors_bio:
            return obj.pourcentage_egalim_hors_bio

    def get_genere_par_cuisine_centrale(self, obj):
        return obj.is_teledeclared_by_cc


class DiagnosticTeledeclaredOpenDataSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(source="teledeclaration_id")
    diagnostic_type = serializers.CharField(source="teledeclaration_type")  # TODO: avoid renaming?
    creation_date = serializers.DateTimeField(source="teledeclaration_date")
    version = serializers.CharField(source="teledeclaration_version")

    canteen_name = serializers.CharField(source="canteen_snapshot.name")
    canteen_siret = serializers.CharField(source="canteen_snapshot.siret")
    canteen_siren_unite_legale = serializers.CharField(source="canteen_snapshot.siren_unite_legale")
    canteen_central_kitchen_siret = serializers.CharField(
        source="canteen_snapshot.central_producer_siret"
    )  # incohérence dans le nom du champ
    canteen_city_insee_code = serializers.CharField(source="canteen_snapshot.city_insee_code")
    canteen_epci = serializers.CharField(source="canteen_snapshot.epci")
    canteen_epci_lib = serializers.CharField(source="canteen_snapshot.epci_lib")
    canteen_pat_list = serializers.SerializerMethodField()
    canteen_pat_lib_list = serializers.SerializerMethodField()
    canteen_department = serializers.CharField(source="canteen_snapshot.department")
    canteen_department_lib = serializers.CharField(source="canteen_snapshot.department_lib")
    canteen_region = serializers.CharField(source="canteen_snapshot.region")
    canteen_region_lib = serializers.CharField(source="canteen_snapshot.region_lib")
    canteen_economic_model = serializers.CharField(source="canteen_snapshot.economic_model")
    canteen_management_type = serializers.CharField(source="canteen_snapshot.management_type")
    canteen_production_type = serializers.CharField(source="canteen_snapshot.production_type")
    canteen_sector_list = serializers.SerializerMethodField()
    canteen_line_ministry = serializers.SerializerMethodField()

    teledeclaration_ratio_bio = serializers.SerializerMethodField()  # TODO: compute & store in DB?
    teledeclaration_ratio_egalim_hors_bio = serializers.SerializerMethodField(
        read_only=True
    )  # TODO: compute & store in DB?

    class Meta:
        model = Diagnostic
        fields = (
            # diagnostic fields
            "id",  # teledeclaration_id
            "diagnostic_type",  # teledeclaration_type
            "teledeclaration_mode",
            "creation_date",  # teledeclaration_date
            "year",
            "version",
            # applicant fields
            "applicant_id",
            # canteen fields
            "canteen_id",
            "canteen_name",
            "canteen_siret",
            "canteen_siren_unite_legale",
            "canteen_central_kitchen_siret",
            "canteen_city_insee_code",
            "canteen_epci",
            "canteen_epci_lib",
            "canteen_pat_list",
            "canteen_pat_lib_list",
            "canteen_department",
            "canteen_department_lib",
            "canteen_region",
            "canteen_region_lib",
            "canteen_economic_model",
            "canteen_management_type",
            "canteen_production_type",
            "canteen_sector_list",
            "canteen_line_ministry",
            # value fields
            "teledeclaration_ratio_bio",
            "teledeclaration_ratio_egalim_hors_bio",
        )

    def get_canteen_pat_list(self, obj):
        return ",".join(obj.canteen_snapshot.get("pat_list", []) or [])

    def get_canteen_pat_lib_list(self, obj):
        return ",".join(obj.canteen_snapshot.get("pat_lib_list", []) or [])

    def get_canteen_sector_list(self, obj):
        return ",".join(obj.canteen_snapshot_sector_lib_list or [])

    def get_canteen_line_ministry(self, obj):
        line_ministry = obj.canteen_snapshot.get("line_ministry", None)
        if line_ministry and line_ministry not in ["autre"]:
            return Canteen.Ministries(line_ministry).label
        return None

    def get_teledeclaration_ratio_bio(self, obj):
        if obj.pourcentage_bio:
            return obj.pourcentage_bio / 100

    def get_teledeclaration_ratio_egalim_hors_bio(self, obj):
        if obj.pourcentage_egalim_hors_bio:
            return obj.pourcentage_egalim_hors_bio / 100
