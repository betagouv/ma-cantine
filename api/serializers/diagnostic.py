import logging
from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from data.models import Diagnostic

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
        total = self.return_value(self, data, "valeur_totale")
        if total is not None and isinstance(total, Decimal):
            bio = self.return_value(self, data, "valeur_bio")
            sustainable = self.return_value(self, data, "valeur_siqo")
            externality_performance = self.return_value(self, data, "valeur_externalites_performance")
            egalim_others = self.return_value(self, data, "valeur_egalim_autres")
            valeur_sum = (bio or 0) + (sustainable or 0) + (externality_performance or 0) + (egalim_others or 0)
            if valeur_sum > total:
                raise serializers.ValidationError(
                    f"La somme des valeurs d'approvisionnement, {valeur_sum}, est plus que le total, {total}"
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
    class Meta:
        model = Diagnostic
        fields = (
            FIELDS
            + ["teledeclaration"]
            + Diagnostic.TELEDECLARATION_FIELDS
            + Diagnostic.CREATION_META_FIELDS
            + Diagnostic.TUNNEL_PROGRESS_FIELDS
        )
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
