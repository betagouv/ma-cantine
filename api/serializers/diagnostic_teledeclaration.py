from rest_framework import serializers

from data.models import Diagnostic
from data.models.geo import Department, Region
from macantine.etl import utils


class DiagnosticTeledeclaredAnalysisSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="teledeclaration_id", read_only=True)
    creation_date = serializers.DateTimeField(source="teledeclaration_date", read_only=True)
    version = serializers.CharField(source="teledeclaration_version", read_only=True)

    canteen_id = serializers.IntegerField(source="canteen_snapshot.id", read_only=True)
    name = serializers.CharField(source="canteen_snapshot.name", read_only=True)
    siret = serializers.CharField(source="canteen_snapshot.siret", read_only=True)
    siren_unite_legale = serializers.CharField(source="canteen_snapshot.siren_unite_legale", read_only=True)
    daily_meal_count = serializers.IntegerField(source="canteen_snapshot.daily_meal_count", read_only=True)
    yearly_meal_count = serializers.IntegerField(source="canteen_snapshot.yearly_meal_count", read_only=True)
    cout_denrees = serializers.SerializerMethodField()
    cuisine_centrale = serializers.SerializerMethodField()
    central_producer_siret = serializers.CharField(source="canteen_snapshot.central_producer_siret", read_only=True)
    code_insee_commune = serializers.CharField(source="canteen_snapshot.city_insee_code", read_only=True)
    # epci = serializers.CharField(source="canteen_snapshot.epci", read_only=True)
    # epci_lib = serializers.CharField(source="canteen_snapshot.epci_lib", read_only=True)
    departement = serializers.CharField(source="canteen_snapshot.department", read_only=True)
    lib_departement = (
        serializers.SerializerMethodField()
    )  # serializers.CharField(source="canteen_snapshot.department_lib", read_only=True)
    region = serializers.CharField(source="canteen_snapshot.region", read_only=True)
    lib_region = (
        serializers.SerializerMethodField()
    )  # serializers.CharField(source="canteen_snapshot.region_lib", read_only=True)
    nbre_cantines_region = serializers.SerializerMethodField()
    objectif_zone_geo = serializers.SerializerMethodField()
    secteur = serializers.SerializerMethodField()
    categorie = serializers.SerializerMethodField()
    line_ministry = serializers.CharField(source="canteen_snapshot.line_ministry", read_only=True)
    spe = serializers.SerializerMethodField()
    modele_economique = serializers.SerializerMethodField()
    management_type = serializers.SerializerMethodField()
    production_type = serializers.CharField(source="canteen_snapshot.production_type", read_only=True)
    declaration_donnees_2021 = serializers.SerializerMethodField()
    declaration_donnees_2022 = serializers.SerializerMethodField()
    declaration_donnees_2023 = serializers.SerializerMethodField()
    declaration_donnees_2024 = serializers.SerializerMethodField()
    declaration_donnees_2025 = serializers.SerializerMethodField()

    valeur_bio = serializers.FloatField(source="valeur_bio_agg", read_only=True)
    valeur_siqo = serializers.FloatField(source="valeur_siqo_agg", read_only=True)
    valeur_externalites_performance = serializers.FloatField(
        source="valeur_externalites_performance_agg", read_only=True
    )
    valeur_egalim_autres = serializers.FloatField(source="valeur_egalim_autres_agg", read_only=True)
    valeur_somme_egalim_avec_bio = serializers.FloatField(source="valeur_egalim_agg", read_only=True)
    valeur_somme_egalim_hors_bio = serializers.SerializerMethodField()
    valeur_viandes_volailles_produits_de_la_mer = serializers.SerializerMethodField()
    valeur_viandes_volailles_produits_de_la_mer_egalim = serializers.SerializerMethodField()
    ratio_produits_de_la_mer_egalim = serializers.SerializerMethodField()
    ratio_viandes_volailles_egalim = serializers.SerializerMethodField()
    ratio_bio = serializers.SerializerMethodField()
    ratio_egalim_avec_bio = serializers.SerializerMethodField()
    ratio_egalim_sans_bio = serializers.SerializerMethodField()
    diag_gaspi = serializers.BooleanField(source="has_waste_diagnostic", read_only=True)
    plan_action_gaspi = serializers.BooleanField(source="has_waste_plan", read_only=True)
    action_gaspi_inscription = serializers.SerializerMethodField()
    action_gaspi_sensibilisation = serializers.SerializerMethodField()
    action_gaspi_formation = serializers.SerializerMethodField()
    action_gaspi_distribution = serializers.SerializerMethodField()
    action_gaspi_portions = serializers.SerializerMethodField()
    action_gaspi_reutilisation = serializers.SerializerMethodField()

    email = serializers.EmailField(source="applicant_snapshot.email", read_only=True)
    tmp_satellites = serializers.ListField(source="satellites_snapshot", read_only=True)
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
            # "epci",
            # "epci_lib",
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
        read_only_fields = fields

    def get_cout_denrees(self, obj):
        return obj.meal_price if obj.meal_price else -1

    def get_cuisine_centrale(self, obj):
        production_type = obj.canteen_snapshot.get("production_type", None)
        if production_type in ["site", "site_cooked_elsewhere"]:
            return "B) non"
        elif production_type in ["central", "central_serving"]:
            return "A) oui"
        else:
            return "C) non renseigné"

    def get_management_type(self, obj):
        management_type = obj.canteen_snapshot.get("management_type", None)
        if management_type:
            if management_type == "direct":
                return "A) directe"
            elif management_type == "conceded":
                return "B) concédée"
            else:
                return "C) non renseigné"

    def get_modele_economique(self, obj):
        economic_model = obj.canteen_snapshot.get("economic_model", None)
        if economic_model:
            if economic_model == "private":
                return "A) privé"
            elif economic_model == "public":
                return "B) public"
            else:
                return "C) non renseigné"

    def get_secteur(self, obj):
        return ",".join(obj.canteen_snapshot_sector_lib_list or [])

    def get_categorie(self, obj):
        return ",".join(obj.canteen.category_lib_list_from_sector_list or [])

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
        return utils.compute_ratio(obj.valeur_produits_de_la_mer_egalim, obj.valeur_produits_de_la_mer)

    def get_ratio_viandes_volailles_egalim(self, obj):
        return utils.compute_ratio(obj.valeur_viandes_volailles_egalim, obj.valeur_viandes_volailles)

    def get_ratio_bio(self, obj):
        return utils.compute_ratio(obj.valeur_bio_agg, obj.valeur_totale)

    def get_ratio_egalim_avec_bio(self, obj):
        return utils.compute_ratio(obj.valeur_egalim_agg, obj.valeur_totale)

    def get_ratio_egalim_sans_bio(self, obj):
        return utils.compute_ratio(self.get_valeur_somme_egalim_hors_bio(obj), obj.valeur_totale)

    def get_genere_par_cuisine_centrale(self, obj):
        return obj.is_teledeclared_by_cc


class DiagnosticTeledeclaredOpenDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="teledeclaration_id", read_only=True)
    diagnostic_type = serializers.CharField(source="teledeclaration_type", read_only=True)  # TODO: avoid renaming?
    creation_date = serializers.DateTimeField(source="teledeclaration_date", read_only=True)
    version = serializers.CharField(source="teledeclaration_version", read_only=True)

    canteen_name = serializers.CharField(source="canteen_snapshot.name", read_only=True)
    canteen_siret = serializers.CharField(source="canteen_snapshot.siret", read_only=True)
    canteen_siren_unite_legale = serializers.CharField(source="canteen_snapshot.siren_unite_legale", read_only=True)
    canteen_central_kitchen_siret = serializers.CharField(
        source="canteen_snapshot.central_producer_siret", read_only=True
    )  # incohérence dans le nom du champ
    canteen_city_insee_code = serializers.CharField(source="canteen_snapshot.city_insee_code", read_only=True)
    canteen_epci = serializers.CharField(source="canteen_snapshot.epci", read_only=True)
    canteen_epci_lib = serializers.CharField(source="canteen_snapshot.epci_lib", read_only=True)
    canteen_department = serializers.CharField(source="canteen_snapshot.department", read_only=True)
    canteen_department_lib = serializers.CharField(source="canteen_snapshot.department_lib", read_only=True)
    canteen_region = serializers.CharField(source="canteen_snapshot.region", read_only=True)
    canteen_region_lib = serializers.CharField(source="canteen_snapshot.region_lib", read_only=True)
    canteen_economic_model = serializers.CharField(source="canteen_snapshot.economic_model", read_only=True)
    canteen_management_type = serializers.CharField(source="canteen_snapshot.management_type", read_only=True)
    canteen_production_type = serializers.CharField(source="canteen_snapshot.production_type", read_only=True)
    canteen_sector_list = serializers.SerializerMethodField(read_only=True)
    canteen_line_ministry = serializers.CharField(source="canteen_snapshot.line_ministry", read_only=True)

    teledeclaration_ratio_bio = serializers.SerializerMethodField(read_only=True)  # TODO: compute & store in DB?
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
        read_only_fields = fields

    def get_canteen_sector_list(self, obj):
        return ",".join(obj.canteen_snapshot_sector_lib_list or [])

    def get_teledeclaration_ratio_bio(self, obj):
        return obj.valeur_bio_agg / obj.valeur_totale

    def get_teledeclaration_ratio_egalim_hors_bio(self, obj):
        return obj.valeur_egalim_hors_bio_agg / obj.valeur_totale
