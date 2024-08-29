import logging
from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from data.models import Canteen, Sector, CanteenImage, Diagnostic
from django.conf import settings
from .diagnostic import PublicDiagnosticSerializer, FullDiagnosticSerializer, CentralKitchenDiagnosticSerializer
from .diagnostic import ApproDiagnosticSerializer
from .diagnostic import PublicApproDiagnosticSerializer, PublicServiceDiagnosticSerializer
from .sector import SectorSerializer
from .user import CanteenManagerSerializer
from .managerinvitation import ManagerInvitationSerializer


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


class PublicationStatusMixin:
    publication_status = serializers.SerializerMethodField(read_only=True)

    def get_publication_status(self, obj):
        if not settings.PUBLISH_BY_DEFAULT:
            return obj.publication_status
        if obj.line_ministry == Canteen.Ministries.ARMEE:
            return Canteen.PublicationStatus.DRAFT
        return Canteen.PublicationStatus.PUBLISHED


class MinimalCanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        read_only_fields = (
            "id",
            "siret",
            "name",
            "publication_status",
        )
        fields = (
            "id",
            "siret",
            "name",
            "publication_status",
        )


class BadgesSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(source="latest_published_year")
    appro = serializers.BooleanField(source="latest_published_appro_diagnostic.appro_badge", default=False)
    waste = serializers.BooleanField(source="latest_published_service_diagnostic.waste_badge", default=False)
    diversification = serializers.BooleanField(
        source="latest_published_service_diagnostic.diversification_badge", default=False
    )
    plastic = serializers.BooleanField(source="latest_published_service_diagnostic.plastic_badge", default=False)
    info = serializers.BooleanField(source="latest_published_service_diagnostic.info_badge", default=False)

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
    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    badges = BadgesSerializer(read_only=True, source="*")
    appro_diagnostic = PublicApproDiagnosticSerializer(read_only=True, source="latest_published_appro_diagnostic")
    lead_image = CanteenImageSerializer()

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "daily_meal_count",
            "production_type",
            "management_type",
            "satellite_canteens_count",
            "region",
            "department",
            "badges",
            "appro_diagnostic",
            "lead_image",
            "is_central_cuisine",
            "is_satellite",
        )


class PublicCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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
            "sectors",
            "daily_meal_count",
            "production_type",
            "management_type",
            "satellite_canteens_count",
            "region",
            "department",
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
        )

    def get_is_managed_by_user(self, obj):
        user = self.context["request"].user
        return user in obj.managers.all()


class ElectedCanteenSerializer(serializers.ModelSerializer, PublicationStatusMixin):
    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    diagnostics = PublicDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    central_kitchen_diagnostics = CentralKitchenDiagnosticSerializer(many=True, read_only=True)
    is_managed_by_user = serializers.SerializerMethodField(read_only=True)
    publication_status = PublicationStatusMixin.publication_status

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "diagnostics",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "daily_meal_count",
            "yearly_meal_count",
            "production_type",
            "satellite_canteens_count",
            "region",
            "department",
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


class SatelliteCanteenSerializer(serializers.ModelSerializer, PublicationStatusMixin):
    sectors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sector.objects.all(), required=False)
    user_can_view = serializers.SerializerMethodField(read_only=True)
    publication_status = PublicationStatusMixin.publication_status

    class Meta:
        model = Canteen
        read_only_fields = ("id",)
        fields = (
            "id",
            "name",
            "siret",
            "daily_meal_count",
            "sectors",
            "user_can_view",
            "publication_status",
        )

    def get_user_can_view(self, obj):
        # thanks to https://stackoverflow.com/questions/59430930/how-can-i-access-request-object-within-a-custom-serializer-field-in-the-django-r
        user = self.context["request"].user
        return obj.managers.filter(pk=user.pk).exists()


class FullCanteenSerializer(serializers.ModelSerializer, PublicationStatusMixin):
    sectors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sector.objects.all(), required=False)
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
    publication_status = PublicationStatusMixin.publication_status

    class Meta:
        model = Canteen

        read_only_fields = (
            "id",
            "region",
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
        )
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "central_kitchen_diagnostics",
            "line_ministry",
            "daily_meal_count",
            "yearly_meal_count",
            "satellite_canteens_count",
            "siret",
            "central_producer_siret",
            "central_kitchen",
            "satellites",
            "management_type",
            "production_type",
            "diagnostics",
            "appro_diagnostics",
            "department",
            "region",
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
            "creation_mtm_source",
            "creation_mtm_campaign",
            "creation_mtm_medium",
            "is_central_cuisine",
            "is_satellite",
            "modification_date",
            "badges",
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


class CanteenSummarySerializer(serializers.ModelSerializer, PublicationStatusMixin):
    lead_image = CanteenImageSerializer()
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    central_kitchen_diagnostics = serializers.SerializerMethodField(read_only=True)
    publication_status = PublicationStatusMixin.publication_status

    class Meta:
        model = Canteen
        my_fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "daily_meal_count",
            "yearly_meal_count",
            "siret",
            "management_type",
            "production_type",
            "department",
            "region",
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
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    action = serializers.CharField(allow_null=True)
    sectors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sector.objects.all(), required=False)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "city",
            "production_type",
            "daily_meal_count",
            "yearly_meal_count",
            "management_type",
            "sectors",
            "line_ministry",
            "satellite_canteens_count",
            "central_producer_siret",
            "action",
            "diagnostics",
        )
        read_only_fields = fields


class CanteenStatusSerializer(serializers.ModelSerializer):
    is_managed_by_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "name",
            "id",
            "siret",
            "is_managed_by_user",
            "can_be_claimed",
        )
        read_only_fields = fields

    def get_is_managed_by_user(self, obj):
        user = self.context["request"].user
        return user in obj.managers.all()


# remember to update TD version if you update this
class CanteenTeledeclarationSerializer(serializers.ModelSerializer):
    sectors = SectorSerializer(many=True, read_only=True)
    central_producer_siret = serializers.SerializerMethodField(read_only=True)
    satellite_canteens_count = serializers.SerializerMethodField(read_only=True)
    line_ministry = serializers.SerializerMethodField(read_only=True)
    daily_meal_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "siret",
            "city_insee_code",
            "department",
            "region",
            "sectors",
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

    def get_line_ministry(self, obj):
        concerned_sectors = obj.sectors.filter(has_line_ministry=True)
        return obj.line_ministry if len(concerned_sectors) > 0 else None

    def get_daily_meal_count(self, obj):
        if obj.production_type == Canteen.ProductionType.CENTRAL:
            return None
        return obj.daily_meal_count


# remember to update TD version if you update this
class SatelliteTeledeclarationSerializer(serializers.ModelSerializer):
    sectors = SectorSerializer(many=True, read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "siret",
            "name",
            "daily_meal_count",
            "yearly_meal_count",
            "sectors",
        )
