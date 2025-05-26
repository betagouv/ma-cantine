from rest_framework import serializers

from data.department_choices import Department
from data.models import Teledeclaration
from data.region_choices import Region


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
    daily_meal_count = serializers.SerializerMethodField()
    yearly_meal_count = serializers.SerializerMethodField()
    management_type = serializers.SerializerMethodField()
    production_type = serializers.SerializerMethodField()
    modele_economique = serializers.SerializerMethodField()
    cuisine_centrale = serializers.SerializerMethodField()
    central_producer_siret = serializers.SerializerMethodField()
    secteur = serializers.SerializerMethodField()
    categorie = serializers.SerializerMethodField()
    satellite_canteens_count = serializers.SerializerMethodField()
    code_insee_commune = serializers.SerializerMethodField()
    departement = serializers.SerializerMethodField()
    lib_departement = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    lib_region = serializers.SerializerMethodField()
    line_ministry = serializers.SerializerMethodField()

    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "declared_data",
            "creation_date",
            "canteen_id",
            "name",
            "daily_meal_count",
            "yearly_meal_count",
            "management_type",
            "production_type",
            "cuisine_centrale",
            "central_producer_siret",
            "modele_economique",
            "secteur",
            "categorie",
            "satellite_canteens_count",
            "code_insee_commune",
            "departement",
            "lib_departement",
            "region",
            "lib_region",
            "line_ministry",
            "year",
            "siret",
            "canteen_siren_unite_legale",
            "value_total_ht",
            "value_bio_ht_agg",
            "value_sustainable_ht_agg",
            "value_externality_performance_ht_agg",
            "value_egalim_others_ht_agg",
            "meal_price",
            "status",
            "applicant_id",
            "diagnostic_id",
            "teledeclaration_mode",
        )
        read_only_fields = fields

    def get_siret(self, obj):
        return obj.canteen_siret

    def get_name(self, obj):
        if "name" in obj.declared_data["canteen"].keys():
            return obj.declared_data["canteen"]["name"]

    def get_daily_meal_count(self, obj):
        if "daily_meal_count" in obj.declared_data["canteen"].keys():
            daily_meal_count = obj.declared_data["canteen"]["daily_meal_count"]
            return int(daily_meal_count) if daily_meal_count else None

    def get_yearly_meal_count(self, obj):
        if "yearly_meal_count" in obj.declared_data["canteen"].keys():
            yearly_meal_count = obj.declared_data["canteen"]["yearly_meal_count"]
            return int(yearly_meal_count) if yearly_meal_count else None

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
            if len(sectors) > 1:
                return "Secteurs multiples"
            elif len(sectors) == 1:
                return sectors[0]["name"]
            else:
                return None

    def get_categorie(self, obj):
        if "sectors" in obj.declared_data["canteen"]:
            category = obj.declared_data["canteen"]["sectors"]
            if len(category) > 1:
                return "Catégories multiples"
            elif len(category) == 1:
                return category[0]["category"]
            else:
                return None

    def get_satellite_canteens_count(self, obj):
        if "satellite_canteens_count" in obj.declared_data["canteen"]:
            satellite_canteens_count = obj.declared_data["canteen"]["satellite_canteens_count"]
            return int(satellite_canteens_count) if satellite_canteens_count else None

    def get_code_insee_commune(self, obj):
        if "city_insee_code" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["city_insee_code"]

    def get_departement(self, obj):
        if "department" in obj.declared_data.keys():
            return obj.declared_data["canteen"]["department"]

    def get_lib_departement(self, obj):
        department = self.get_departement(obj)
        return Department(department).label.split(" - ")[1].lstrip() if department else None

    def get_region(self, obj):
        if "region" in obj.declared_data.keys():
            return obj.declared_data["canteen"]["region"]

    def get_lib_region(self, obj):
        region = self.get_region(obj)
        return Region(region).label.split(" - ")[1].lstrip() if region else None

    def get_line_ministry(self, obj):
        if "line_ministry" in obj.declared_data["canteen"]:
            return obj.declared_data["canteen"]["line_ministry"]


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


class TeledeclarationOpenDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "declared_data",
            "creation_date",
            "modification_date",
            "year",
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
            "canteen_id",
            "diagnostic_id",
            "teledeclaration_mode",
        )
        read_only_fields = fields
