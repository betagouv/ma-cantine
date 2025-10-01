import logging
from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from api.serializers.utils import (
    extract_category_from_dict_sectors,
    extract_sector_from_dict_sectors,
)
from data.department_choices import Department
from data.models import Diagnostic
from data.region_choices import Region
from macantine.etl import utils

from .teledeclaration import ShortTeledeclarationSerializer
from .utils import appro_to_percentages

logger = logging.getLogger(__name__)

FIELDS = (
    Diagnostic.META_FIELDS
    + Diagnostic.SIMPLE_APPRO_FIELDS
    + Diagnostic.COMPLETE_APPRO_FIELDS
    + Diagnostic.NON_APPRO_FIELDS
)
REQUIRED_FIELDS = ("year",)


class DiagnosticSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if (
            "total_leftovers" in representation
            and representation["total_leftovers"] is not None
            and representation["total_leftovers"] != ""
        ):
            representation["total_leftovers"] = representation["total_leftovers"] * 1000
        return representation

    def to_internal_value(self, data):
        if "total_leftovers" in data and data["total_leftovers"] is not None and data["total_leftovers"] != "":
            try:
                value = Decimal(repr(data["total_leftovers"]))
                data["total_leftovers"] = value / 1000
            except InvalidOperation:
                raise serializers.ValidationError(
                    {"total_leftovers": ["Assurez-vous que cette valeur est un chiffre décimal."]}
                )
            except Exception as e:
                logger.exception(e)
                raise serializers.ValidationError(
                    {
                        "total_leftovers": [
                            "Une erreur est survenue. Assurez-vous que cette valeur est un chiffre décimal, et contactez-nous si l'erreur persiste."
                        ]
                    }
                )
            if data["total_leftovers"].as_tuple().exponent < -5:
                raise serializers.ValidationError(
                    {"total_leftovers": ["Assurez-vous qu'il n'y a pas plus de 2 chiffres après la virgule."]}
                )
        validated_data = super().to_internal_value(data)
        return validated_data


class CentralKitchenDiagnosticSerializer(DiagnosticSerializer):
    """
    This serializer masks financial data and gives the basic information on appro as percentages
    """

    class Meta:
        fields = FIELDS
        read_only_fields = fields
        model = Diagnostic

    def to_representation(self, instance):
        """
        To facilitate the handling and merging of diagnostic in the front-end, we will include only appro
        fields if the central kitchen diagnostic is set to mode: APPRO
        This method pops non-appro fields if that is the case from the JSON representation
        """
        representation = super().to_representation(instance)
        representation = appro_to_percentages(representation, instance)
        if instance.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO:
            [representation.pop(field, "") for field in Diagnostic.NON_APPRO_FIELDS]
        if instance.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE:
            [representation.pop(field, "") for field in Diagnostic.COMPLETE_APPRO_FIELDS]
        return representation


class PublicDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = FIELDS
        read_ony_fields = FIELDS

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return appro_to_percentages(representation, instance)


class PublicApproDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS
        read_only_fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return appro_to_percentages(representation, instance)


class PublicServiceDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.NON_APPRO_FIELDS
        read_only_fields = Diagnostic.META_FIELDS + Diagnostic.NON_APPRO_FIELDS


class ManagerDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        read_only_fields = ("id",)
        fields = (
            FIELDS + Diagnostic.MATOMO_FIELDS + Diagnostic.CREATION_META_FIELDS + Diagnostic.TUNNEL_PROGRESS_FIELDS
        )

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        if action == "create":
            for field in REQUIRED_FIELDS:
                self.fields[field].required = True
        else:
            for field in Diagnostic.MATOMO_FIELDS:
                self.fields.pop(field)

    def validate(self, data):
        # TODO: move these rules to the model
        total = self.return_value(self, data, "value_total_ht")
        if total is not None and isinstance(total, Decimal):
            bio = self.return_value(self, data, "value_bio_ht")
            sustainable = self.return_value(self, data, "value_sustainable_ht")
            externality_performance = self.return_value(self, data, "value_externality_performance_ht")
            egalim_others = self.return_value(self, data, "value_egalim_others_ht")
            value_sum = (bio or 0) + (sustainable or 0) + (externality_performance or 0) + (egalim_others or 0)
            if value_sum > total:
                raise serializers.ValidationError(
                    f"La somme des valeurs d'approvisionnement, {value_sum}, est plus que le total, {total}"
                )
            # TODO: test meat and fish too?
        return data

    @staticmethod
    def return_value(serializer, data, field_name):
        if field_name in data:
            return data.get(field_name)
        elif serializer.instance and getattr(serializer.instance, field_name):
            return getattr(serializer.instance, field_name)


class FullDiagnosticSerializer(DiagnosticSerializer):
    teledeclaration = ShortTeledeclarationSerializer(source="latest_submitted_teledeclaration")

    class Meta:
        model = Diagnostic
        fields = FIELDS + ["teledeclaration"] + Diagnostic.CREATION_META_FIELDS + Diagnostic.TUNNEL_PROGRESS_FIELDS
        read_only_fields = fields


class SimpleTeledeclarationDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS + Diagnostic.NON_APPRO_FIELDS
        read_only_fields = fields


class CompleteTeledeclarationDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.COMPLETE_APPRO_FIELDS + Diagnostic.NON_APPRO_FIELDS
        read_only_fields = fields


class ApproDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS + Diagnostic.COMPLETE_APPRO_FIELDS
        read_only_fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS + Diagnostic.COMPLETE_APPRO_FIELDS

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return appro_to_percentages(representation, instance, remove_values=False)


class ApproDeferredTeledeclarationDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.NON_APPRO_FIELDS
        read_only_fields = fields


class SimpleApproOnlyTeledeclarationDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS
        read_only_fields = fields


class CompleteApproOnlyTeledeclarationDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.COMPLETE_APPRO_FIELDS
        read_only_fields = fields


class DiagnosticAndCanteenSerializer(FullDiagnosticSerializer):
    canteen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Diagnostic
        fields = tuple(FullDiagnosticSerializer().fields) + ("canteen",)

    def get_canteen(self, obj):
        from .canteen import FullCanteenSerializer

        return FullCanteenSerializer(obj.canteen).data


class DiagnosticAnalysisSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="teledeclaration_id", read_only=True)
    creation_date = serializers.DateTimeField(source="teledeclaration_date", read_only=True)
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
    satellite_canteens_count = serializers.IntegerField(
        source="canteen_snapshot.satellite_canteens_count", read_only=True
    )
    modele_economique = serializers.SerializerMethodField()
    management_type = serializers.SerializerMethodField()
    production_type = serializers.CharField(source="canteen_snapshot.production_type", read_only=True)
    declaration_donnees_2021 = serializers.SerializerMethodField()
    declaration_donnees_2022 = serializers.SerializerMethodField()
    declaration_donnees_2023 = serializers.SerializerMethodField()
    declaration_donnees_2024 = serializers.SerializerMethodField()

    value_bio_ht = serializers.FloatField(source="value_bio_ht_agg", read_only=True)
    value_sustainable_ht = serializers.FloatField(source="value_sustainable_ht_agg", read_only=True)
    value_externality_performance_ht = serializers.FloatField(
        source="value_externality_performance_ht_agg", read_only=True
    )
    value_egalim_others_ht = serializers.FloatField(source="value_egalim_others_ht_agg", read_only=True)
    value_somme_egalim_avec_bio_ht = serializers.FloatField(source="value_egalim_ht_agg", read_only=True)
    value_somme_egalim_hors_bio_ht = serializers.SerializerMethodField()
    value_meat_and_fish_ht = serializers.SerializerMethodField()
    value_meat_and_fish_egalim_ht = serializers.SerializerMethodField()
    ratio_egalim_fish = serializers.SerializerMethodField()
    ratio_egalim_meat_poultry = serializers.SerializerMethodField()
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
            "id",  # teledeclaration_id  # TODO: replace with diagnostic_id
            "diagnostic_type",
            "teledeclaration_mode",
            "creation_date",  # teledeclaration_date
            "year",
            "creation_source",
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
            "satellite_canteens_count",
            "modele_economique",
            "management_type",
            "production_type",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
            # value fields
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
            # applicant fields
            "email",
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
        sectors = obj.canteen_snapshot.get("sectors", None)
        if sectors:
            return extract_sector_from_dict_sectors(sectors)

    def get_categorie(self, obj):
        categories = obj.canteen_snapshot.get("sectors", None)
        if categories:
            return extract_category_from_dict_sectors(categories)

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

    def get_value_somme_egalim_hors_bio_ht(self, obj):
        return utils.sum_int_and_none(
            [
                obj.value_sustainable_ht_agg,
                obj.value_externality_performance_ht_agg,
                obj.value_egalim_others_ht_agg,
            ]
        )

    def get_value_meat_and_fish_ht(self, obj):
        return utils.sum_int_and_none([obj.value_meat_poultry_ht, obj.value_fish_ht])

    def get_value_meat_and_fish_egalim_ht(self, obj):
        return utils.sum_int_and_none([obj.value_meat_poultry_egalim_ht, obj.value_fish_egalim_ht])

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

    def get_ratio_egalim_fish(self, obj):
        return utils.compute_ratio(obj.value_fish_egalim_ht, obj.value_fish_ht)

    def get_ratio_egalim_meat_poultry(self, obj):
        return utils.compute_ratio(obj.value_meat_poultry_egalim_ht, obj.value_meat_poultry_ht)

    def get_ratio_bio(self, obj):
        return utils.compute_ratio(obj.value_bio_ht_agg, obj.value_total_ht)

    def get_ratio_egalim_avec_bio(self, obj):
        return utils.compute_ratio(obj.value_egalim_ht_agg, obj.value_total_ht)

    def get_ratio_egalim_sans_bio(self, obj):
        return utils.compute_ratio(self.get_value_somme_egalim_hors_bio_ht(obj), obj.value_total_ht)

    def get_genere_par_cuisine_centrale(self, obj):
        return obj.is_teledeclared_by_cc


class DiagnosticOpenDataSerializer(serializers.ModelSerializer):
    diagnostic_type = serializers.CharField(source="teledeclaration_type", read_only=True)  # TODO: avoid renaming?
    creation_date = serializers.DateTimeField(source="teledeclaration_date", read_only=True)  # TODO: avoid renaming?
    version = serializers.CharField(source="teledeclaration_version", read_only=True)  # TODO: avoid renaming?

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
    canteen_satellite_canteens_count = serializers.IntegerField(
        source="canteen_snapshot.satellite_canteens_count", read_only=True
    )
    canteen_economic_model = serializers.CharField(source="canteen_snapshot.economic_model", read_only=True)
    canteen_management_type = serializers.CharField(source="canteen_snapshot.management_type", read_only=True)
    canteen_production_type = serializers.CharField(source="canteen_snapshot.production_type", read_only=True)
    canteen_sectors = serializers.ListField(source="canteen_snapshot.sectors", read_only=True)
    canteen_line_ministry = serializers.CharField(source="canteen_snapshot.line_ministry", read_only=True)

    teledeclaration_ratio_bio = serializers.SerializerMethodField(read_only=True)  # TODO: compute & store in DB?
    teledeclaration_ratio_egalim_hors_bio = serializers.SerializerMethodField(
        read_only=True
    )  # TODO: compute & store in DB?

    class Meta:
        model = Diagnostic
        fields = (
            "id",
            "diagnostic_type",
            "teledeclaration_mode",
            "creation_date",
            "year",
            "version",
            "teledeclaration_id",
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
            "canteen_satellite_canteens_count",
            "canteen_economic_model",
            "canteen_management_type",
            "canteen_production_type",
            "canteen_sectors",
            "canteen_line_ministry",
            # value fields
            "teledeclaration_ratio_bio",
            "teledeclaration_ratio_egalim_hors_bio",
        )
        read_only_fields = fields

    def get_teledeclaration_ratio_bio(self, obj):
        return obj.value_bio_ht_agg / obj.value_total_ht

    def get_teledeclaration_ratio_egalim_hors_bio(self, obj):
        return obj.value_egalim_hors_bio_ht_agg / obj.value_total_ht
