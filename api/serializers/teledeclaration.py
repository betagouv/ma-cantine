from rest_framework import serializers

from api.serializers.utils import (
    extract_category_from_dict_sectors,
    extract_sector_from_dict_sectors,
    safe_to_float,
)
from data.department_choices import Department
from data.models import Diagnostic, Teledeclaration
from data.region_choices import Region
from macantine.etl import utils


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


class TeledeclarationAnalysisSerializer(serializers.ModelSerializer):
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
    genere_par_cuisine_centrale = serializers.SerializerMethodField()
    declaration_donnees_2021 = serializers.SerializerMethodField()
    declaration_donnees_2022 = serializers.SerializerMethodField()
    declaration_donnees_2023 = serializers.SerializerMethodField()
    declaration_donnees_2024 = serializers.SerializerMethodField()

    # Data related to the appro
    value_bio_ht = serializers.SerializerMethodField()
    value_sustainable_ht = serializers.SerializerMethodField()
    value_externality_performance_ht = serializers.SerializerMethodField()
    value_egalim_others_ht = serializers.SerializerMethodField()
    value_meat_poultry_ht = serializers.SerializerMethodField()
    value_meat_poultry_france_ht = serializers.SerializerMethodField()
    value_meat_poultry_egalim_ht = serializers.SerializerMethodField()
    value_fish_ht = serializers.SerializerMethodField()
    value_fish_egalim_ht = serializers.SerializerMethodField()
    value_somme_egalim_avec_bio_ht = serializers.SerializerMethodField()
    value_somme_egalim_hors_bio_ht = serializers.SerializerMethodField()
    value_meat_and_fish_ht = serializers.SerializerMethodField()
    value_meat_and_fish_egalim_ht = serializers.SerializerMethodField()
    service_type = serializers.SerializerMethodField()
    vegetarian_weekly_recurrence = serializers.SerializerMethodField()
    vegetarian_menu_type = serializers.SerializerMethodField()
    ratio_egalim_fish = serializers.SerializerMethodField()
    ratio_egalim_meat_poultry = serializers.SerializerMethodField()
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

    # Metadata
    creation_source = serializers.SerializerMethodField()

    # Extra
    # Data related to the satellites, necessary to flatten the dataset
    tmp_satellites = serializers.SerializerMethodField()

    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "declared_data",
            "creation_date",
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
            "genere_par_cuisine_centrale",
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
            "value_total_ht",
            "value_bio_ht",
            "value_sustainable_ht",
            "value_externality_performance_ht",
            "value_egalim_others_ht",
            "value_meat_poultry_ht",
            "value_meat_poultry_france_ht",
            "value_meat_poultry_egalim_ht",
            "value_fish_ht",
            "value_fish_egalim_ht",
            "value_somme_egalim_avec_bio_ht",
            "value_somme_egalim_hors_bio_ht",
            "value_meat_and_fish_ht",
            "value_meat_and_fish_egalim_ht",
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
            "ratio_egalim_fish",
            "ratio_egalim_meat_poultry",
            "ratio_bio",
            "ratio_egalim_avec_bio",
            "ratio_egalim_sans_bio",
            "email",
            "tmp_satellites",
            "creation_source",
        )
        read_only_fields = fields

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

    def get_genere_par_cuisine_centrale(self, obj):
        return obj.is_declared_by_cc

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

    def get_value_bio_ht(self, obj):
        return obj.value_bio_ht_agg

    def get_value_sustainable_ht(self, obj):
        return obj.value_sustainable_ht_agg

    def get_value_externality_performance_ht(self, obj):
        return obj.value_externality_performance_ht_agg

    def get_value_egalim_others_ht(self, obj):
        return obj.value_egalim_others_ht_agg

    def get_value_meat_poultry_ht(self, obj):
        return safe_to_float(obj.diagnostic.value_meat_poultry_ht)

    def get_value_meat_poultry_france_ht(self, obj):
        return safe_to_float(obj.diagnostic.value_meat_poultry_france_ht)

    def get_value_meat_poultry_egalim_ht(self, obj):
        return safe_to_float(obj.diagnostic.value_meat_poultry_egalim_ht)

    def get_value_fish_ht(self, obj):
        return safe_to_float(obj.diagnostic.value_fish_ht)

    def get_value_fish_egalim_ht(self, obj):
        return safe_to_float(obj.diagnostic.value_fish_egalim_ht)

    def get_value_somme_egalim_avec_bio_ht(self, obj):
        return utils.sum_int_and_none([self.get_value_somme_egalim_hors_bio_ht(obj), self.get_value_bio_ht(obj)])

    def get_value_somme_egalim_hors_bio_ht(self, obj):
        return utils.sum_int_and_none(
            [
                self.get_value_externality_performance_ht(obj),
                self.get_value_sustainable_ht(obj),
                self.get_value_egalim_others_ht(obj),
            ]
        )

    def get_value_meat_and_fish_ht(self, obj):
        return utils.sum_int_and_none([self.get_value_meat_poultry_ht(obj), self.get_value_fish_ht(obj)])

    def get_value_meat_and_fish_egalim_ht(self, obj):
        return utils.sum_int_and_none([self.get_value_meat_poultry_egalim_ht(obj), self.get_value_fish_egalim_ht(obj)])

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

    def get_plan_action_gaspi(self, obj):
        if "has_waste_plan" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["has_waste_plan"]

    def get_action_gaspi_inscription(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            return "INSCRIPTION" in obj.declared_data["teledeclaration"]["waste_actions"]

    def get_action_gaspi_sensibilisation(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            return "AWARENESS" in obj.declared_data["teledeclaration"]["waste_actions"]

    def get_action_gaspi_formation(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            return "TRAINING" in obj.declared_data["teledeclaration"]["waste_actions"]

    def get_action_gaspi_distribution(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            return "DISTRIBUTION" in obj.declared_data["teledeclaration"]["waste_actions"]

    def get_action_gaspi_portions(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            return "PORTIONS" in obj.declared_data["teledeclaration"]["waste_actions"]

    def get_action_gaspi_reutilisation(self, obj):
        if "waste_actions" in obj.declared_data["teledeclaration"]:
            return "REUSE" in obj.declared_data["teledeclaration"]["waste_actions"]

    def get_ratio_egalim_fish(self, obj):
        return utils.compute_ratio(self.get_value_fish_egalim_ht(obj), self.get_value_fish_ht(obj))

    def get_ratio_egalim_meat_poultry(self, obj):
        return utils.compute_ratio(self.get_value_meat_poultry_egalim_ht(obj), self.get_value_meat_poultry_ht(obj))

    def get_ratio_bio(self, obj):
        return utils.compute_ratio(self.get_value_bio_ht(obj), obj.value_total_ht)

    def get_ratio_egalim_avec_bio(self, obj):
        return utils.compute_ratio(self.get_value_somme_egalim_avec_bio_ht(obj), obj.value_total_ht)

    def get_ratio_egalim_sans_bio(self, obj):
        return utils.compute_ratio(self.get_value_somme_egalim_hors_bio_ht(obj), obj.value_total_ht)

    def get_email(self, obj):
        if "email" in obj.declared_data["applicant"]:
            return obj.declared_data["applicant"]["email"]

    def get_tmp_satellites(self, obj):
        if "satellites" in obj.declared_data:
            return obj.declared_data["satellites"]

    def get_creation_source(self, obj):
        return obj.diagnostic.creation_source


class TeledeclarationOpenDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "year",
            "creation_date",
            "canteen_id",
            "declared_data",
            "canteen_siret",
            "canteen_siren_unite_legale",
            "value_total_ht",
            "value_bio_ht_agg",
            "value_sustainable_ht_agg",
            "value_externality_performance_ht_agg",
            "value_egalim_others_ht_agg",
            "yearly_meal_count",
            "meal_price",
            "status",
            "applicant_id",
            "diagnostic_id",
            "teledeclaration_mode",
        )
        read_only_fields = fields
