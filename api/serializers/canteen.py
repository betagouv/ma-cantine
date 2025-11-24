import logging
import os

from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from data.models import Canteen, CanteenImage, Diagnostic, SectorM2M, Sector

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
from .sector import SectorM2MSerializer
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
    publication_status = serializers.CharField(read_only=True, source="publication_status_display_to_public")

    class Meta:
        model = Canteen
        read_only_fields = (
            "id",
            "name",
            "siret",
            "publication_status",
        )
        fields = (
            "id",
            "name",
            "siret",
            "publication_status",
        )


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
    appro_diagnostic = PublicApproDiagnosticSerializer(read_only=True, source="latest_published_appro_diagnostic")
    lead_image = CanteenImageSerializer()
    badges = BadgesSerializer(read_only=True, source="*")

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
            "sector_list",
            "daily_meal_count",
            "production_type",
            "management_type",
            "satellite_canteens_count",
            "appro_diagnostic",
            "lead_image",
            "is_central_cuisine",
            "is_satellite",
            "badges",
        )


class PublicCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    appro_diagnostics = PublicApproDiagnosticSerializer(
        many=True, read_only=True, source="published_appro_diagnostics"
    )
    service_diagnostics = PublicServiceDiagnosticSerializer(
        many=True, read_only=True, source="published_service_diagnostics"
    )
    central_kitchen = MinimalCanteenSerializer(read_only=True)
    logo = Base64ImageField(required=False, allow_null=True)
    images = MediaListSerializer(child=CanteenImageSerializer(), read_only=True)
    is_managed_by_user = serializers.SerializerMethodField(read_only=True)
    badges = BadgesSerializer(read_only=True, source="*")
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
            "sectors",  # from "sectors_m2m"
            "sector_list",
            "daily_meal_count",
            "production_type",
            "management_type",
            "satellite_canteens_count",
            "logo",
            "images",
            "publication_comments",
            "quality_comments",
            "waste_comments",
            "diversification_comments",
            "plastics_comments",
            "information_comments",
            "can_be_claimed",
            "is_managed_by_user",
            "central_kitchen",
            "badges",
            "resource_actions",
        )

    def get_is_managed_by_user(self, obj):
        user = self.context["request"].user
        return user in obj.managers.all()


class ElectedCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    diagnostics = PublicDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    central_kitchen_diagnostics = CentralKitchenDiagnosticSerializer(many=True, read_only=True)
    is_managed_by_user = serializers.SerializerMethodField(read_only=True)
    publication_status = serializers.CharField(read_only=True, source="publication_status_display_to_public")

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
            "satellite_canteens_count",
            "quality_comments",
            "waste_comments",
            "diversification_comments",
            "plastics_comments",
            "information_comments",
            "is_managed_by_user",
            "central_kitchen_diagnostics",
            "publication_status",
        )

    def get_is_managed_by_user(self, obj):
        user = self.context["request"].user
        return user in obj.managers.all()


class SatelliteCanteenSerializer(serializers.ModelSerializer):
    user_can_view = serializers.SerializerMethodField(read_only=True)
    publication_status = serializers.CharField(read_only=True, source="publication_status_display_to_public")

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
            "daily_meal_count",
            "user_can_view",
            "publication_status",
        )

    def get_user_can_view(self, obj):
        # thanks to https://stackoverflow.com/questions/59430930/how-can-i-access-request-object-within-a-custom-serializer-field-in-the-django-r
        user = self.context["request"].user
        return obj.managers.filter(pk=user.pk).exists()


class FullCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(
        source="sectors_m2m", many=True, queryset=SectorM2M.objects.all(), required=False
    )
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    appro_diagnostics = ApproDiagnosticSerializer(many=True, read_only=True)
    logo = Base64ImageField(required=False, allow_null=True)
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(many=True, read_only=True, source="managerinvitation_set")
    images = MediaListSerializer(child=CanteenImageSerializer(), required=False)
    central_kitchen_diagnostics = serializers.SerializerMethodField(read_only=True)
    central_kitchen = MinimalCanteenSerializer(read_only=True)
    satellites = MinimalCanteenSerializer(many=True, read_only=True)
    badges = BadgesSerializer(read_only=True, source="*")
    resource_actions = ResourceActionFullSerializer(many=True, read_only=True)
    publication_status = serializers.CharField(read_only=True, source="publication_status_display_to_public")

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
            "central_kitchen_diagnostics",
            "central_kitchen",
            "satellites",
            "is_central_cuisine",
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
            "sector_list",
            "central_kitchen_diagnostics",
            "line_ministry",
            "daily_meal_count",
            "yearly_meal_count",
            "satellite_canteens_count",
            "siret",
            "siren_unite_legale",
            "central_producer_siret",
            "central_kitchen",
            "satellites",
            "management_type",
            "production_type",
            "diagnostics",
            "appro_diagnostics",
            "logo",
            "images",
            "managers",
            "manager_invitations",
            "publication_status",
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
            "is_central_cuisine",
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

    def get_central_kitchen_diagnostics(self, obj):
        # Ideally we would also check the status of the satellite canteen and
        # the central cuisine, for now we omit this check. For now it is the
        # responsibility of the frontend to use this information.
        if not obj.central_producer_siret or not obj.production_type == Canteen.ProductionType.ON_SITE_CENTRAL:
            return None
        try:
            diagnostics = Diagnostic.objects.filter(
                canteen__siret=obj.central_producer_siret,
                central_kitchen_diagnostic_mode__in=[
                    Diagnostic.CentralKitchenDiagnosticMode.ALL,
                    Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                ],
            )

            return CentralKitchenDiagnosticSerializer(diagnostics, many=True).data
        except Canteen.DoesNotExist:
            return None
        except Canteen.MultipleObjectsReturned as e:
            logger.exception(f"Multiple canteens returned when obtaining the central_producer_siret field {e}")
            return None


class CanteenSummarySerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    lead_image = CanteenImageSerializer()
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    central_kitchen_diagnostics = serializers.SerializerMethodField(read_only=True)
    publication_status = serializers.CharField(read_only=True, source="publication_status_display_to_public")

    class Meta:
        model = Canteen
        my_fields = (
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
            "publication_status",
            "economic_model",
            "is_central_cuisine",
            "is_satellite",
            "modification_date",
            "lead_image",
            # the following can still be improved
            "diagnostics",
            "central_kitchen_diagnostics",  # can return a TD status instead of diagnostics
        )
        fields = my_fields
        read_only_fields = my_fields

    def get_central_kitchen_diagnostics(self, obj):
        # Ideally we would also check the status of the satellite canteen and
        # the central cuisine, for now we omit this check. For now it is the
        # responsibility of the frontend to use this information.
        if not obj.central_producer_siret or not obj.production_type == Canteen.ProductionType.ON_SITE_CENTRAL:
            return None
        try:
            diagnostics = Diagnostic.objects.filter(
                canteen__siret=obj.central_producer_siret,
                central_kitchen_diagnostic_mode__in=[
                    Diagnostic.CentralKitchenDiagnosticMode.ALL,
                    Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                ],
            )

            return CentralKitchenDiagnosticSerializer(diagnostics, many=True).data
        except Canteen.DoesNotExist:
            return None
        except Canteen.MultipleObjectsReturned as e:
            logger.exception(f"Multiple canteens returned when obtaining the central_producer_siret field {e}")
            return None


class CanteenPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        read_only_fields = (
            "id",
            "name",
        )
        fields = (
            "id",
            "name",
        )


class ManagingTeamSerializer(serializers.ModelSerializer):
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(many=True, read_only=True, source="managerinvitation_set")

    class Meta:
        model = Canteen
        fields = ("id", "managers", "manager_invitations")


class CanteenActionsSerializer(serializers.ModelSerializer):
    # TODO: is it worth moving the job of fetching the specific diag required to the front?
    sectors = serializers.PrimaryKeyRelatedField(source="sectors_m2m", many=True, read_only=True)
    publication_status = serializers.CharField(read_only=True, source="publication_status_display_to_public")
    lead_image = CanteenImageSerializer()
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
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
            "satellite_canteens_count",
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
            "action",  # annotate
        )
        read_only_fields = fields


class CanteenStatusSerializer(serializers.ModelSerializer):
    is_managed_by_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "city",
            "postal_code",
            "department",
            "is_managed_by_user",
            "can_be_claimed",
            "production_type",
        )
        read_only_fields = fields

    def get_is_managed_by_user(self, obj):
        user = self.context["request"].user
        return user in obj.managers.all()


# remember to update TD version if you update this
class CanteenTeledeclarationSerializer(serializers.ModelSerializer):
    sectors = SectorM2MSerializer(source="sectors_m2m", many=True, read_only=True)
    central_producer_siret = serializers.SerializerMethodField(read_only=True)
    satellite_canteens_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "siren_unite_legale",
            "city_insee_code",
            # "postal_code",
            # "epci",
            # "epci_lib",
            # "pat",
            # "pat_lib",
            "department",
            # "department_lib",
            "region",
            # "region_lib",
            "sectors",  # from "sectors_m2m"
            "line_ministry",
            "daily_meal_count",
            "yearly_meal_count",
            "production_type",
            "management_type",
            "economic_model",
            "satellite_canteens_count",
            "central_producer_siret",
        )

    def get_central_producer_siret(self, obj):
        if not obj.production_type == Canteen.ProductionType.ON_SITE_CENTRAL:
            return None
        return obj.central_producer_siret

    def get_satellite_canteens_count(self, obj):
        if (
            not obj.production_type == Canteen.ProductionType.CENTRAL
            and not obj.production_type == Canteen.ProductionType.CENTRAL_SERVING
        ):
            return None
        return obj.satellite_canteens_count


# remember to update TD version if you update this
class SatelliteTeledeclarationSerializer(serializers.ModelSerializer):
    sectors = SectorM2MSerializer(source="sectors_m2m", many=True, read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "siren_unite_legale",
            "daily_meal_count",
            "yearly_meal_count",
            "sectors",  # from "sectors_m2m"
        )


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
    nombre_satellites = serializers.IntegerField(source="satellite_canteens_count")
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
            "nombre_satellites",
            "siret_cuisine_centrale",
            "ministere_tutelle",
            "spe",
            "secteur",
            "categorie",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
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
        return ",".join([Sector(sector).label for sector in obj.sector_list])

    def get_categorie(self, obj):
        return ",".join([category.label for category in obj.category_list_from_sector_list])

    def get_adresses_gestionnaires(self, obj):
        emails = [manager.email for manager in obj.managers.all()]
        return ",".join(emails)


class CanteenOpenDataSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField(read_only=True)
    sector_list = serializers.SerializerMethodField(source="sector_list", read_only=True)
    sectors = serializers.SerializerMethodField(source="sectors_m2m", read_only=True)
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
            "satellite_canteens_count",
            "central_producer_siret",
            "creation_date",
            "daily_meal_count",
            "yearly_meal_count",
            "line_ministry",
            "modification_date",
            "logo",
            "sector_list",
            "sectors",  # from "sectors_m2m"
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024",
            "active_on_ma_cantine",
        )

    def get_logo(self, obj):
        bucket_url = os.environ.get("CELLAR_HOST")
        bucket_name = os.environ.get("CELLAR_BUCKET_NAME")

        if obj.logo:
            return f"{bucket_url}/{bucket_name}/media/{obj.logo}"
        return ""

    def get_sector_list(self, obj):
        return [Sector(sector).label for sector in obj.sector_list]

    def get_sectors(self, obj):
        return [sector.name for sector in obj.sectors_m2m.all()]

    def get_active_on_ma_cantine(self, obj):
        return obj.managers.exists()


class CanteenMinistriesSerializer(serializers.Serializer):
    value = serializers.ChoiceField(choices=Canteen.Ministries.choices)
    name = serializers.CharField()
