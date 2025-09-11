import logging
from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from data.models import Diagnostic
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
        return (
            utils.sum_int_and_none(
                [
                    obj.value_sustainable_ht_agg,
                    obj.value_externality_performance_ht_agg,
                    obj.value_egalim_others_ht_agg,
                ]
            )
            / obj.value_total_ht
        )
