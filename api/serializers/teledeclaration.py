from rest_framework import serializers

from data.models import Teledeclaration


class ShortTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "status",
        )
        read_only_fields = fields
<<<<<<< HEAD
=======


class TeledeclarationAnalysisSerializer(serializers.ModelSerializer):
    # Metadata
    creation_source = serializers.SerializerMethodField()

    # Data related to the canteen
    name = serializers.SerializerMethodField()
    siret = serializers.SerializerMethodField()
    siren_unite_legale = serializers.SerializerMethodField()
    daily_meal_count = serializers.SerializerMethodField()
    yearly_meal_count = serializers.SerializerMethodField()
    cout_denrees = serializers.SerializerMethodField()
    management_type = serializers.SerializerMethodField()
    production_type = serializers.SerializerMethodField()
    modele_economique = serializers.SerializerMethodField()
    cuisine_centrale = serializers.SerializerMethodField()
    diagnostic_type = serializers.SerializerMethodField()
    central_producer_siret = serializers.SerializerMethodField()
    secteur = serializers.SerializerMethodField()
    categorie = serializers.SerializerMethodField()
    satellite_canteens_count = serializers.SerializerMethodField()
    code_insee_commune = serializers.SerializerMethodField()
    departement = serializers.SerializerMethodField()
    lib_departement = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    lib_region = serializers.SerializerMethodField()
    nbre_cantines_region = serializers.SerializerMethodField()
    objectif_zone_geo = serializers.SerializerMethodField()
    line_ministry = serializers.SerializerMethodField()
    spe = serializers.SerializerMethodField()
    declaration_donnees_2021 = serializers.SerializerMethodField()
    declaration_donnees_2022 = serializers.SerializerMethodField()
    declaration_donnees_2023 = serializers.SerializerMethodField()
    declaration_donnees_2024 = serializers.SerializerMethodField()

    # Data related to the appro
    value_bio = serializers.SerializerMethodField()
    value_siqo = serializers.SerializerMethodField()
    value_externalites_performance = serializers.SerializerMethodField()
    value_egalim_autres = serializers.SerializerMethodField()
    value_viandes_volailles = serializers.SerializerMethodField()
    value_viandes_volailles_france = serializers.SerializerMethodField()
    value_viandes_volailles_egalim = serializers.SerializerMethodField()
    value_produits_de_la_mer = serializers.SerializerMethodField()
    value_produits_de_la_mer_egalim = serializers.SerializerMethodField()
    value_somme_egalim_avec_bio = serializers.SerializerMethodField()
    value_somme_egalim_hors_bio = serializers.SerializerMethodField()
    value_viandes_volailles_produits_de_la_mer = serializers.SerializerMethodField()
    value_viandes_volailles_produits_de_la_mer_egalim = serializers.SerializerMethodField()
    service_type = serializers.SerializerMethodField()
    vegetarian_weekly_recurrence = serializers.SerializerMethodField()
    vegetarian_menu_type = serializers.SerializerMethodField()
    ratio_egalim_produits_de_la_mer = serializers.SerializerMethodField()
    ratio_egalim_viandes_volailles = serializers.SerializerMethodField()
    ratio_bio = serializers.SerializerMethodField()
    ratio_egalim_avec_bio = serializers.SerializerMethodField()
    ratio_egalim_sans_bio = serializers.SerializerMethodField()

    # Data related to the waste (gaspillage)
    diag_gaspi = serializers.SerializerMethodField()
    plan_action_gaspi = serializers.SerializerMethodField()
    action_gaspi_inscription = serializers.SerializerMethodField()
    action_gaspi_sensibilisation = serializers.SerializerMethodField()
    action_gaspi_formation = serializers.SerializerMethodField()
    action_gaspi_distribution = serializers.SerializerMethodField()
    action_gaspi_portions = serializers.SerializerMethodField()
    action_gaspi_reutilisation = serializers.SerializerMethodField()

    # Data related to the applicant
    email = serializers.SerializerMethodField()

    # Extra
    # Data related to the satellites, necessary to flatten the dataset
    tmp_satellites = serializers.SerializerMethodField()
    genere_par_cuisine_centrale = serializers.SerializerMethodField()

    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "declared_data",
            "creation_date",
            "creation_source",
            "canteen_id",
            "name",
            "siret",
            "siren_unite_legale",
            "daily_meal_count",
            "yearly_meal_count",
            "cout_denrees",
            "management_type",
            "production_type",
            "cuisine_centrale",
            "modele_economique",
            "central_producer_siret",
            "diagnostic_type",
            "secteur",
            "categorie",
            "satellite_canteens_count",
            "code_insee_commune",
            "departement",
            "lib_departement",
            "region",
            "lib_region",
            "nbre_cantines_region",
            "objectif_zone_geo",
            "line_ministry",
            "spe",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
            "year",
            "status",
            "applicant_id",
            "diagnostic_id",
            "value_totale",
            "value_bio",
            "value_siqo",
            "value_externalites_performance",
            "value_egalim_autres",
            "value_viandes_volailles",
            "value_viandes_volailles_france",
            "value_viandes_volailles_egalim",
            "value_produits_de_la_mer",
            "value_produits_de_la_mer_egalim",
            "value_somme_egalim_avec_bio",
            "value_somme_egalim_hors_bio",
            "value_viandes_et_produits_de_la_mer",
            "value_viandes_et_produits_de_la_mer_egalim",
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
            "ratio_egalim_produits_de_la_mer",
            "ratio_egalim_viandes_volailles",
            "ratio_bio",
            "ratio_egalim_avec_bio",
            "ratio_egalim_sans_bio",
            "email",
            "tmp_satellites",
            "genere_par_cuisine_centrale",
        )
        read_only_fields = fields

    def get_creation_source(self, obj):
        return obj.diagnostic.creation_source

    def get_name(self, obj):
        if "name" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["name"]

    def get_siret(self, obj):
        return obj.canteen_siret

    def get_siren_unite_legale(self, obj):
        return obj.canteen_siren_unite_legale

    def get_daily_meal_count(self, obj):
        if "daily_meal_count" in obj.declared_data["canteen"]:
            daily_meal_count = obj.declared_data["canteen"]["daily_meal_count"]
            return int(daily_meal_count) if daily_meal_count else None

    def get_yearly_meal_count(self, obj):
        if "yearly_meal_count" in obj.declared_data["canteen"]:
            yearly_meal_count = obj.declared_data["canteen"]["yearly_meal_count"]
            return int(yearly_meal_count) if yearly_meal_count else None

    def get_cout_denrees(self, obj):
        return obj.meal_price if obj.meal_price else -1

    def get_management_type(self, obj):
        if "management_type" in obj.declared_data["canteen"]:
            value = obj.declared_data["canteen"]["management_type"]
            if value == "direct":
                return "A) directe"
            elif value == "conceded":
                return "B) concédée"
            else:
                return "C) non renseigné"

    def get_production_type(self, obj):
        if "production_type" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["production_type"]

    def get_cuisine_centrale(self, obj):
        value = self.get_production_type(obj)
        if value in ["site", "site_cooked_elsewhere"]:
            return "B) non"
        elif value in ["central", "central_serving"]:
            return "A) oui"
        else:
            return "C) non renseigné"

    def get_diagnostic_type(self, obj):
        if "diagnostic_type" in obj.declared_data["teledeclaration"]:
            return (
                obj.declared_data["teledeclaration"]["diagnostic_type"]
                if obj.declared_data["teledeclaration"]["diagnostic_type"]
                and obj.declared_data["teledeclaration"]["diagnostic_type"] != ""
                else Diagnostic.DiagnosticType.SIMPLE
            )

    def get_central_producer_siret(self, obj):
        if "central_producer_siret" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["central_producer_siret"]

    def get_modele_economique(self, obj):
        if "economic_model" in obj.declared_data["canteen"]:
            value = obj.declared_data["canteen"]["economic_model"]
            if value == "private":
                return "A) privé"
            elif value == "public":
                return "B) public"
            else:
                return "C) non renseigné"

    def get_secteur(self, obj):
        if "sectors" in obj.declared_data["canteen"]:
            sectors = obj.declared_data["canteen"]["sectors"]
            return extract_sector_from_dict_sectors(sectors)

    def get_categorie(self, obj):
        if "sectors" in obj.declared_data["canteen"]:
            categories = obj.declared_data["canteen"]["sectors"]
            return extract_category_from_dict_sectors(categories)

    def get_satellite_canteens_count(self, obj):
        if "satellite_canteens_count" in obj.declared_data["canteen"]:
            satellite_canteens_count = obj.declared_data["canteen"]["satellite_canteens_count"]
            return int(satellite_canteens_count) if satellite_canteens_count else None

    def get_code_insee_commune(self, obj):
        if "city_insee_code" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["city_insee_code"]

    def get_departement(self, obj):
        if "department" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["department"]

    def get_lib_departement(self, obj):
        department = self.get_departement(obj)
        return Department(department).label.split(" - ")[1].lstrip() if department else None

    def get_region(self, obj):
        if "region" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["region"]

    def get_lib_region(self, obj):
        region = self.get_region(obj)
        return Region(region).label.split(" - ")[1].lstrip() if region else None

    def get_nbre_cantines_region(self, obj):
        return utils.get_nbre_cantines_region(self.get_region(obj))

    def get_objectif_zone_geo(self, obj):
        return utils.get_objectif_zone_geo(self.get_departement(obj))

    def get_line_ministry(self, obj):
        if "line_ministry" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["line_ministry"]

    def get_spe(self, obj):
        line_ministry = self.get_line_ministry(obj)
        return "Oui" if line_ministry else "Non"

    def get_declaration_donnees_2021(self, obj):
        return obj.canteen.declaration_donnees_2021

    def get_declaration_donnees_2022(self, obj):
        return obj.canteen.declaration_donnees_2022

    def get_declaration_donnees_2023(self, obj):
        return obj.canteen.declaration_donnees_2023

    def get_declaration_donnees_2024(self, obj):
        return obj.canteen.declaration_donnees_2024

    def get_value_bio(self, obj):
        return obj.value_bio_agg

    def get_value_siqo(self, obj):
        return obj.value_siqo_agg

    def get_value_externalites_performance(self, obj):
        return obj.value_externalites_performance_agg

    def get_value_egalim_autres(self, obj):
        return obj.value_egalim_autres_agg

    def get_value_viandes_volailles(self, obj):
        return safe_to_float(obj.diagnostic.value_viandes_volailles)

    def get_value_viandes_volailles_france(self, obj):
        return safe_to_float(obj.diagnostic.value_viandes_volailles_france)

    def get_value_viandes_volailles_egalim(self, obj):
        return safe_to_float(obj.diagnostic.value_viandes_volailles_egalim)

    def get_value_produits_de_la_mer(self, obj):
        return safe_to_float(obj.diagnostic.value_produits_de_la_mer)

    def get_value_produits_de_la_mer_egalim(self, obj):
        return safe_to_float(obj.diagnostic.value_produits_de_la_mer_egalim)

    def get_value_somme_egalim_avec_bio(self, obj):
        return utils.sum_int_and_none([self.get_value_somme_egalim_hors_bio(obj), self.get_value_bio(obj)])

    def get_value_somme_egalim_hors_bio(self, obj):
        return utils.sum_int_and_none(
            [
                self.get_value_externalites_performance(obj),
                self.get_value_siqo(obj),
                self.get_value_egalim_autres(obj),
            ]
        )

    def get_value_viandes_volailles_produits_de_la_mer(self, obj):
        return utils.sum_int_and_none([self.get_value_viandes_volailles(obj), self.get_value_produits_de_la_mer(obj)])

    def get_value_viandes_volailles_produits_de_la_mer_egalim(self, obj):
        return utils.sum_int_and_none(
            [self.get_value_viandes_volailles_egalim(obj), self.get_value_produits_de_la_mer_egalim(obj)]
        )

    def get_service_type(self, obj):
        if "service_type" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["service_type"]

    def get_vegetarian_weekly_recurrence(self, obj):
        if "vegetarian_weekly_recurrence" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["vegetarian_weekly_recurrence"]

    def get_vegetarian_menu_type(self, obj):
        if "vegetarian_menu_type" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["vegetarian_menu_type"]

    def get_diag_gaspi(self, obj):
        if "has_waste_diagnostic" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["has_waste_diagnostic"]
        return False

    def get_plan_action_gaspi(self, obj):
        if "has_waste_plan" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["has_waste_plan"]
        return False

    def get_action_gaspi_inscription(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            waste_actions = obj.declared_data["teledeclaration"]["waste_actions"]
            if waste_actions:
                return Diagnostic.WasteActions.INSCRIPTION in waste_actions
        return False

    def get_action_gaspi_sensibilisation(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            waste_actions = obj.declared_data["teledeclaration"]["waste_actions"]
            if waste_actions:
                return Diagnostic.WasteActions.AWARENESS in obj.declared_data["teledeclaration"]["waste_actions"]
        return False

    def get_action_gaspi_formation(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            waste_actions = obj.declared_data["teledeclaration"]["waste_actions"]
            if waste_actions:
                return Diagnostic.WasteActions.TRAINING in obj.declared_data["teledeclaration"]["waste_actions"]
        return False

    def get_action_gaspi_distribution(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            waste_actions = obj.declared_data["teledeclaration"]["waste_actions"]
            if waste_actions:
                return Diagnostic.WasteActions.DISTRIBUTION in obj.declared_data["teledeclaration"]["waste_actions"]
        return False

    def get_action_gaspi_portions(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            waste_actions = obj.declared_data["teledeclaration"]["waste_actions"]
            if waste_actions:
                return Diagnostic.WasteActions.PORTIONS in obj.declared_data["teledeclaration"]["waste_actions"]
        return False

    def get_action_gaspi_reutilisation(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            waste_actions = obj.declared_data["teledeclaration"]["waste_actions"]
            if waste_actions:
                return Diagnostic.WasteActions.REUSE in obj.declared_data["teledeclaration"]["waste_actions"]
        return False

    def get_ratio_egalim_produits_de_la_mer(self, obj):
        return utils.compute_ratio(
            self.get_value_produits_de_la_mer_egalim(obj), self.get_value_produits_de_la_mer(obj)
        )

    def get_ratio_egalim_viandes_volailles(self, obj):
        return utils.compute_ratio(self.get_value_viandes_volailles_egalim(obj), self.get_value_viandes_volailles(obj))

    def get_ratio_bio(self, obj):
        return utils.compute_ratio(self.get_value_bio(obj), obj.value_totale)

    def get_ratio_egalim_avec_bio(self, obj):
        return utils.compute_ratio(self.get_value_somme_egalim_avec_bio(obj), obj.value_total)

    def get_ratio_egalim_sans_bio(self, obj):
        return utils.compute_ratio(self.get_value_somme_egalim_hors_bio(obj), obj.value_total)

    def get_email(self, obj):
        if "email" in obj.declared_data["applicant"]:
            return obj.declared_data["applicant"]["email"]

    def get_tmp_satellites(self, obj):
        if "satellites" in obj.declared_data:
            return obj.declared_data["satellites"]

    def get_genere_par_cuisine_centrale(self, obj):
        return obj.is_declared_by_cc


class TeledeclarationOpenDataSerializer(serializers.ModelSerializer):
    teledeclaration_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "year",
            "creation_date",
            "teledeclaration_id",
            "canteen_id",
            "declared_data",
            "canteen_siret",
            "canteen_siren_unite_legale",
            "value_totale",
            "value_bio_agg",
            "value_siqo_agg",
            "value_externalites_performance_agg",
            "value_egalim_autres_agg",
            "yearly_meal_count",
            "meal_price",
            "status",
            "applicant_id",
            "diagnostic_id",
            "teledeclaration_mode",
        )
        read_only_fields = fields
>>>>>>> ad608e80a (Cleanup)
