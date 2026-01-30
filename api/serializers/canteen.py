import logging
import os

from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from data.models import Canteen, CanteenImage, SectorM2M

from .diagnostic import (
    ApproDiagnosticSerializer,
    CentralKitchenDiagnosticSerializer,
    FullDiagnosticSerializer,
    PublicApproDiagnosticSerializer,
    PublicDiagnosticSerializer,
    PublicServiceDiagnosticSerializer,
)
from .managerinvitation import ManagerInvitationSerializer
from .resourceaction import ResourceActionFullSerializer
from .user import CanteenManagerSerializer

logger = logging.getLogger(__name__)


class CanteenImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CanteenImage
        fields = (
            "id",
            "image",
            "alt_text",
        )


class MediaListSerializer(serializers.ListSerializer):
    """
    For linked models and list serializers, we need to specify the update behaviour since
    Django Rest Framework does not do it :
    https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update
    """

    def update(self, instance, validated_data):
        instance_mapping = {instance.id: instance for instance in instance}

        media = []

        # New media will be created and existing media will be updated.
        for item in validated_data:
            element = instance_mapping.get(item.get("id"), None)
            if element is None:
                media.append(self.child.create(item))
            else:
                media.append(self.child.update(element, item))

        # Media that was removed will be also removed from the database.
        data_mapping = {item["id"]: item for item in validated_data if item.get("id")}
        for element_id, element in instance_mapping.items():
            if element_id not in data_mapping:
                element.delete()

        return media


class MinimalCanteenSerializer(serializers.ModelSerializer):
    publication_status = serializers.CharField(source="publication_status_display_to_public", read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "siren_unite_legale",
            "publication_status",  # property
        )
        read_only_fields = fields


class BadgesSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(source="latest_published_year")
    appro = serializers.BooleanField(source="latest_published_appro_diagnostic.appro_badge", default=None)
    waste = serializers.BooleanField(source="latest_published_service_diagnostic.waste_badge", default=None)
    diversification = serializers.BooleanField(
        source="latest_published_service_diagnostic.diversification_badge", default=None
    )
    plastic = serializers.BooleanField(source="latest_published_service_diagnostic.plastic_badge", default=None)
    info = serializers.BooleanField(source="latest_published_service_diagnostic.info_badge", default=None)

    class Meta:
        model = Canteen
        fields = (
            "year",
            "appro",
            "waste",
            "diversification",
            "plastic",
            "info",
        )


class PublicCanteenPreviewSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    appro_diagnostic = PublicApproDiagnosticSerializer(source="latest_published_appro_diagnostic", read_only=True)
    lead_image = CanteenImageSerializer()
    badges = BadgesSerializer(source="*", read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "sector_list",
            "sectors",  # from "sectors_m2m"
            "daily_meal_count",
            "production_type",
            "management_type",
            "appro_diagnostic",
            "lead_image",
            "is_satellite",
            "badges",
        )


class PublicCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    appro_diagnostics = PublicApproDiagnosticSerializer(
        source="published_appro_diagnostics", many=True, read_only=True
    )
    service_diagnostics = PublicServiceDiagnosticSerializer(
        source="published_service_diagnostics", many=True, read_only=True
    )
    central_kitchen = MinimalCanteenSerializer(read_only=True)
    logo = Base64ImageField(required=False, allow_null=True)
    images = MediaListSerializer(child=CanteenImageSerializer(), read_only=True)
    is_managed_by_user = serializers.BooleanField(read_only=True)
    badges = BadgesSerializer(source="*", read_only=True)
    resource_actions = ResourceActionFullSerializer(many=True, read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "appro_diagnostics",
            "service_diagnostics",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "sector_list",
            "sectors",  # from "sectors_m2m"
            "daily_meal_count",
            "production_type",
            "management_type",
            "logo",
            "images",
            "publication_comments",
            "quality_comments",
            "waste_comments",
            "diversification_comments",
            "plastics_comments",
            "information_comments",
            "can_be_claimed",  # property
            "is_managed_by_user",  # annotate
            "central_kitchen",
            "badges",
            "resource_actions",
        )


class ElectedCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    diagnostics = PublicDiagnosticSerializer(many=True, read_only=True)
    central_kitchen_diagnostics = CentralKitchenDiagnosticSerializer(many=True, read_only=True)
    is_managed_by_user = serializers.BooleanField(read_only=True)
    publication_status = serializers.CharField(source="publication_status_display_to_public", read_only=True)

    class Meta:
        model = Canteen
        read_only_fields = ("publication_status",)
        fields = (
            "id",
            "name",
            "siret",
            "diagnostics",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "sectors",  # from "sectors_m2m"
            "daily_meal_count",
            "yearly_meal_count",
            "production_type",
            "quality_comments",
            "waste_comments",
            "diversification_comments",
            "plastics_comments",
            "information_comments",
            "is_managed_by_user",  # annotate
            "central_kitchen_diagnostics",
            "publication_status",  # property
        )


class SatelliteCanteenSerializer(serializers.ModelSerializer):
    publication_status = serializers.CharField(source="publication_status_display_to_public", read_only=True)
    is_managed_by_user = serializers.BooleanField(read_only=True)
    action = serializers.CharField(allow_null=True)

    class Meta:
        model = Canteen
        read_only_fields = (
            "id",
            "publication_status",
        )
        fields = (
            "id",
            "name",
            "siret",
            "siren_unite_legale",
            "city",
            "postal_code",
            "daily_meal_count",
            "can_be_claimed",
            "publication_status",  # property
            "is_managed_by_user",  # annotate
            "action",  # annotate
        )


class FullCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(
        source="sectors_m2m", many=True, queryset=SectorM2M.objects.all(), required=False
    )
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True)
    appro_diagnostics = ApproDiagnosticSerializer(many=True, read_only=True)
    logo = Base64ImageField(required=False, allow_null=True)
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(source="managerinvitation_set", many=True, read_only=True)
    images = MediaListSerializer(child=CanteenImageSerializer(), required=False)
    groupe = MinimalCanteenSerializer(read_only=True)
    central_kitchen = MinimalCanteenSerializer(read_only=True)
    central_kitchen_diagnostics = CentralKitchenDiagnosticSerializer(many=True, read_only=True)
    satellites = MinimalCanteenSerializer(many=True, read_only=True)
    satellites_missing_data_count = serializers.IntegerField(read_only=True)
    satellites_already_teledeclared_count = serializers.IntegerField(read_only=True)
    badges = BadgesSerializer(source="*", read_only=True)
    resource_actions = ResourceActionFullSerializer(many=True, read_only=True)
    publication_status = serializers.CharField(source="publication_status_display_to_public", read_only=True)

    class Meta:
        model = Canteen
        read_only_fields = (
            "id",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department_lib",
            "region",
            "region_lib",
            "managers",
            "manager_invitations",
            "publication_status",
            "groupe",
            "central_kitchen",
            "central_kitchen_diagnostics",
            "satellites",
            "satellites_count",
            "satellites_missing_data_count",
            "satellites_already_teledeclared_count",
            "is_satellite",
            "modification_date",
            "badges",
            "resource_actions",
        )
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "sector_list",
            "sectors",  # from "sectors_m2m"
            "line_ministry",
            "daily_meal_count",
            "yearly_meal_count",
            "siret",
            "siren_unite_legale",
            "groupe",
            "central_producer_siret",
            "central_kitchen",
            "central_kitchen_diagnostics",
            "satellites",
            "satellites_count",  # property
            "satellites_missing_data_count",  # property
            "satellites_already_teledeclared_count",  # property
            "management_type",
            "production_type",
            "diagnostics",
            "appro_diagnostics",
            "logo",
            "images",
            "managers",
            "manager_invitations",
            "publication_status",  # property
            "redacted_appro_years",
            "publication_comments",
            "quality_comments",
            "waste_comments",
            "diversification_comments",
            "plastics_comments",
            "information_comments",
            "economic_model",
            "reservation_expe_participant",
            "vegetarian_expe_participant",
            "creation_source",
            "creation_mtm_source",
            "creation_mtm_campaign",
            "creation_mtm_medium",
            "is_satellite",
            "modification_date",
            "badges",
            "resource_actions",
        )

        extra_kwargs = {"name": {"required": True}, "siret": {"required": True}}

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        if action != "create":
            self.fields.pop("creation_mtm_source")
            self.fields.pop("creation_mtm_campaign")
            self.fields.pop("creation_mtm_medium")

    def update(self, instance, validated_data):
        if "images" not in validated_data:
            return super().update(instance, validated_data)

        image_validated_data = validated_data.pop("images", None)
        canteen = super().update(instance, validated_data)

        if image_validated_data is not None:
            canteen_image_serializer = self.fields["images"]
            for item in image_validated_data:
                item["canteen"] = canteen
            canteen_image_serializer.update(canteen.images.all(), image_validated_data)

        return canteen

    def create(self, validated_data):
        if "images" not in validated_data:
            return super().create(validated_data)

        image_validated_data = validated_data.pop("images", None)
        canteen = super().create(validated_data)

        if image_validated_data is not None:
            canteen_image_serializer = self.fields["images"]
            for item in image_validated_data:
                item["canteen"] = canteen
            canteen_image_serializer.update(canteen.images.all(), image_validated_data)

        return canteen


class CanteenSummarySerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    lead_image = CanteenImageSerializer()
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True)
    central_kitchen_diagnostics = CentralKitchenDiagnosticSerializer(many=True, read_only=True)
    publication_status = serializers.CharField(source="publication_status_display_to_public", read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "sectors",
            "daily_meal_count",
            "yearly_meal_count",
            "siret",
            "siren_unite_legale",
            "management_type",
            "production_type",
            "publication_status",  # property
            "economic_model",
            "is_satellite",
            "modification_date",
            "lead_image",
            # the following can still be improved
            "diagnostics",
            "central_kitchen_diagnostics",  # can return a TD status instead of diagnostics
        )
        read_only_fields = fields


class CanteenPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class ManagingTeamSerializer(serializers.ModelSerializer):
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(source="managerinvitation_set", many=True, read_only=True)

    class Meta:
        model = Canteen
        fields = ("id", "managers", "manager_invitations")


class CanteenActionsSerializer(serializers.ModelSerializer):
    # TODO: is it worth moving the job of fetching the specific diag required to the front?
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    publication_status = serializers.CharField(source="publication_status_display_to_public", read_only=True)
    lead_image = CanteenImageSerializer()
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True)
    action = serializers.CharField(allow_null=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "sectors",  # from "sectors_m2m"
            "line_ministry",
            "daily_meal_count",
            "yearly_meal_count",
            "siret",
            "siren_unite_legale",
            "central_producer_siret",
            "management_type",
            "production_type",
            "economic_model",
            "publication_status",  # property
            "lead_image",  # M2O
            "diagnostics",  # M2O
            "action",  # annotate
        )
        read_only_fields = fields


class CanteenActionsLightSerializer(serializers.ModelSerializer):
    action = serializers.CharField(allow_null=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "siren_unite_legale",
            "city",
            "postal_code",
            "production_type",
            "groupe",
            "satellites_count",  # property
            "satellites_missing_data_count",  # property
            "action",  # annotate
        )
        read_only_fields = fields


class CanteenStatusSerializer(serializers.ModelSerializer):
    is_managed_by_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "city",
            "postal_code",
            "department",
            "production_type",
            "groupe",
            "can_be_claimed",  # property
            "is_managed_by_user",  # annotate
        )
        read_only_fields = fields


CANTEEN_TELEDECLARATION_SNAPSHOT_FIELDS = (
    "id",
    "name",
    "siret",
    "siren_unite_legale",
    "city_insee_code",
    "department",
    "region",
    "daily_meal_count",
    "yearly_meal_count",
    "sector_list",
    "line_ministry",
    "production_type",
    "management_type",
    "economic_model",
    "central_producer_siret",
    "groupe_id",
    "is_filled",
)


# remember to update TD version if you update this
class CanteenTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = CANTEEN_TELEDECLARATION_SNAPSHOT_FIELDS


# remember to update TD version if you update this
class SatelliteTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = CANTEEN_TELEDECLARATION_SNAPSHOT_FIELDS


class CanteenAnalysisSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(source="name")
    code_insee_commune = serializers.CharField(source="city_insee_code")
    libelle_commune = serializers.CharField(source="city")
    pat_liste = serializers.SerializerMethodField()
    pat_lib_liste = serializers.SerializerMethodField()
    departement = serializers.CharField(source="department")
    departement_lib = serializers.CharField(source="department_lib")
    nbre_repas_jour = serializers.IntegerField(source="daily_meal_count")
    nbre_repas_an = serializers.IntegerField(source="yearly_meal_count")
    modele_economique = serializers.SerializerMethodField()
    type_gestion = serializers.SerializerMethodField()
    type_production = serializers.SerializerMethodField()
    siret_cuisine_centrale = serializers.CharField(source="central_producer_siret")
    ministere_tutelle = serializers.SerializerMethodField()
    spe = serializers.SerializerMethodField()
    secteur = serializers.SerializerMethodField()
    categorie = serializers.SerializerMethodField()
    date_creation = serializers.DateTimeField(source="creation_date")
    date_modification = serializers.DateTimeField(source="modification_date")
    adresses_gestionnaires = serializers.SerializerMethodField()

    class Meta:
        model = Canteen
        fields = (
            "id",
            "nom",
            "siret",
            "siren_unite_legale",
            "code_insee_commune",
            "libelle_commune",
            "epci",
            "epci_lib",
            "pat_liste",
            "pat_lib_liste",
            "departement",
            "departement_lib",
            "region",
            "region_lib",
            "date_creation",
            "date_modification",
            "nbre_repas_jour",
            "nbre_repas_an",
            "modele_economique",
            "type_gestion",
            "type_production",
            "siret_cuisine_centrale",
            "groupe_id",
            "ministere_tutelle",
            "spe",
            "secteur",
            "categorie",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
            "declaration_donnees_2025",
            "adresses_gestionnaires",
        )
        read_only_fields = fields

    def get_pat_liste(self, obj):
        return ",".join(obj.pat_list)

    def get_pat_lib_liste(self, obj):
        return ",".join(obj.pat_lib_list)

    def get_modele_economique(self, obj):
        if obj.economic_model:
            return Canteen.EconomicModel(obj.economic_model).label
        return None

    def get_type_gestion(self, obj):
        if obj.management_type:
            return Canteen.ManagementType(obj.management_type).label
        return None

    def get_type_production(self, obj):
        if obj.production_type:
            return Canteen.ProductionType(obj.production_type).label
        return None

    def get_ministere_tutelle(self, obj):
        if obj.line_ministry:
            return Canteen.Ministries(obj.line_ministry).label
        return None

    def get_spe(self, obj):
        return "Oui" if obj.is_spe else "Non"

    def get_secteur(self, obj):
        return ",".join(obj.sector_lib_list)

    def get_categorie(self, obj):
        return ",".join(obj.category_lib_list_from_sector_list)

    def get_adresses_gestionnaires(self, obj):
        emails = [manager.email for manager in obj.managers.all()]
        return ",".join(emails)


class CanteenOpenDataSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField(read_only=True)
    sector_list = serializers.ListField(source="sector_lib_list", read_only=True)  # property
    active_on_ma_cantine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "siren_unite_legale",
            "city",
            "city_insee_code",
            "postal_code",
            "epci",
            "epci_lib",
            "pat_list",
            "pat_lib_list",
            "department",
            "department_lib",
            "region",
            "region_lib",
            "economic_model",
            "management_type",
            "production_type",
            "central_producer_siret",
            "groupe_id",
            "creation_date",
            "daily_meal_count",
            "yearly_meal_count",
            "sector_list",
            "line_ministry",
            "modification_date",
            "logo",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
            "declaration_donnees_2025",
            "active_on_ma_cantine",
        )

    def get_logo(self, obj):
        bucket_url = os.environ.get("CELLAR_HOST")
        bucket_name = os.environ.get("CELLAR_BUCKET_NAME")

        if obj.logo:
            return f"{bucket_url}/{bucket_name}/media/{obj.logo}"
        return ""

    def get_active_on_ma_cantine(self, obj):
        return obj.managers.exists()


class CanteenMinistriesSerializer(serializers.Serializer):
    value = serializers.ChoiceField(choices=Canteen.Ministries.choices)
    name = serializers.CharField()
