import logging
from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from data.models import Diagnostic

from .teledeclaration import ShortTeledeclarationSerializer
from .utils import COMPLETE_APPRO_FIELDS, appro_to_percentages

logger = logging.getLogger(__name__)

SIMPLE_APPRO_FIELDS = (
    "value_total_ht",
    "value_bio_ht",
    "value_sustainable_ht",
    "value_externality_performance_ht",
    "value_egalim_others_ht",
    "value_meat_poultry_ht",
    "value_meat_poultry_egalim_ht",
    "value_meat_poultry_france_ht",
    "value_fish_ht",
    "value_fish_egalim_ht",
)

NON_APPRO_FIELDS = (
    "has_waste_diagnostic",
    "has_waste_plan",
    "waste_actions",
    "other_waste_action",
    "has_donation_agreement",
    "has_waste_measures",
    "total_leftovers",
    "duration_leftovers_measurement",
    "bread_leftovers",
    "served_leftovers",
    "unserved_leftovers",
    "side_leftovers",
    "donation_frequency",
    "donation_quantity",
    "donation_food_type",
    "other_waste_comments",
    "has_diversification_plan",
    "diversification_plan_actions",
    "vegetarian_weekly_recurrence",
    "vegetarian_menu_type",
    "vegetarian_menu_bases",
    "cooking_plastic_substituted",
    "serving_plastic_substituted",
    "plastic_bottles_substituted",
    "plastic_tableware_substituted",
    "communication_supports",
    "other_communication_support",
    "communication_support_url",
    "communicates_on_food_plan",
    "communicates_on_food_quality",
    "communication_frequency",
)

META_FIELDS = (
    "id",
    "canteen_id",
    "year",
    "diagnostic_type",
    "central_kitchen_diagnostic_mode",
    "is_teledeclared",
)

CREATION_META_FIELDS = (
    "creation_date",
    "modification_date",
    "creation_source",
)

TUNNEL_PROGRESS_FIELDS = (
    "tunnel_appro",
    "tunnel_waste",
    "tunnel_plastic",
    "tunnel_diversification",
    "tunnel_info",
)

FIELDS = META_FIELDS + SIMPLE_APPRO_FIELDS + COMPLETE_APPRO_FIELDS + NON_APPRO_FIELDS

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
            [representation.pop(field, "") for field in NON_APPRO_FIELDS]
        if instance.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE:
            [representation.pop(field, "") for field in COMPLETE_APPRO_FIELDS]
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
        fields = META_FIELDS + SIMPLE_APPRO_FIELDS
        read_ony_fields = META_FIELDS + SIMPLE_APPRO_FIELDS

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return appro_to_percentages(representation, instance)


class PublicServiceDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + NON_APPRO_FIELDS
        read_ony_fields = META_FIELDS + NON_APPRO_FIELDS


class ManagerDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        read_only_fields = ("id",)
        fields = (
            FIELDS
            + (
                "creation_mtm_source",
                "creation_mtm_campaign",
                "creation_mtm_medium",
            )
            + CREATION_META_FIELDS
            + TUNNEL_PROGRESS_FIELDS
        )

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        if action == "create":
            for field in REQUIRED_FIELDS:
                self.fields[field].required = True
        else:
            self.fields.pop("creation_mtm_source")
            self.fields.pop("creation_mtm_campaign")
            self.fields.pop("creation_mtm_medium")

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
        fields = FIELDS + ("teledeclaration",) + CREATION_META_FIELDS + TUNNEL_PROGRESS_FIELDS
        read_only_fields = fields


class SimpleTeledeclarationDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + SIMPLE_APPRO_FIELDS + NON_APPRO_FIELDS
        read_only_fields = fields


class CompleteTeledeclarationDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + COMPLETE_APPRO_FIELDS + NON_APPRO_FIELDS
        read_only_fields = fields


class ApproDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + SIMPLE_APPRO_FIELDS + COMPLETE_APPRO_FIELDS
        read_ony_fields = META_FIELDS + SIMPLE_APPRO_FIELDS + COMPLETE_APPRO_FIELDS

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return appro_to_percentages(representation, instance, remove_values=False)


class ApproDeferredTeledeclarationDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + NON_APPRO_FIELDS
        read_only_fields = fields


class SimpleApproOnlyTeledeclarationDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + SIMPLE_APPRO_FIELDS
        read_only_fields = fields


class CompleteApproOnlyTeledeclarationDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = META_FIELDS + COMPLETE_APPRO_FIELDS
        read_only_fields = fields


class DiagnosticAndCanteenSerializer(FullDiagnosticSerializer):
    canteen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Diagnostic
        fields = tuple(FullDiagnosticSerializer().fields) + ("canteen",)

    def get_canteen(self, obj):
        from .canteen import FullCanteenSerializer

        return FullCanteenSerializer(obj.canteen).data
