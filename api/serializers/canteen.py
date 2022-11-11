from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from data.models import Canteen, Sector, CanteenImage
from .diagnostic import PublicDiagnosticSerializer, FullDiagnosticSerializer
from .user import CanteenManagerSerializer
from .managerinvitation import ManagerInvitationSerializer


class CanteenImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CanteenImage
        fields = (
            "id",
            "image",
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


class PublicCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    diagnostics = PublicDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    logo = Base64ImageField(required=False, allow_null=True)
    images = MediaListSerializer(child=CanteenImageSerializer(), read_only=True)
    can_be_claimed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "diagnostics",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "daily_meal_count",
            "production_type",
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
        )

    def get_can_be_claimed(self, obj):
        return not obj.managers.exists()


class SatelliteCanteenSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sector.objects.all(), required=False)
    user_can_view = serializers.SerializerMethodField(read_only=True)

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
        )

    def get_user_can_view(self, obj):
        # thanks to https://stackoverflow.com/questions/59430930/how-can-i-access-request-object-within-a-custom-serializer-field-in-the-django-r
        user = self.context["request"].user
        return obj.managers.filter(pk=user.pk).exists()


class FullCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sector.objects.all(), required=False)
    diagnostics = FullDiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")
    logo = Base64ImageField(required=False, allow_null=True)
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(many=True, read_only=True, source="managerinvitation_set")
    images = MediaListSerializer(child=CanteenImageSerializer(), required=False)

    class Meta:
        model = Canteen
        read_only_fields = (
            "id",
            "region",
            "managers",
            "manager_invitations",
            "publication_status",
            "publication_comments",
            "quality_comments",
            "waste_comments",
            "diversification_comments",
            "plastics_comments",
            "information_comments",
        )
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "line_ministry",
            "daily_meal_count",
            "yearly_meal_count",
            "satellite_canteens_count",
            "siret",
            "central_producer_siret",
            "management_type",
            "production_type",
            "diagnostics",
            "department",
            "region",
            "logo",
            "images",
            "managers",
            "manager_invitations",
            "publication_status",
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
        )

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

    class Meta:
        model = Canteen
        fields = ("id", "name", "production_type", "action", "diagnostics")
        read_only_fields = fields
