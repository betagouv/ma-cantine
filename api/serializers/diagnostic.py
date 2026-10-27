import logging
from decimal import Decimal, InvalidOperation

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from api.serializers.utils import ReadOnlySerializerMixin, set_help_text_from_verbose_name
from data.models import Diagnostic

from .teledeclaration import ShortTeledeclarationSerializer

logger = logging.getLogger(__name__)

# v1 keeps the English names of the fields renamed in French (used by the Vue 2 tunnel)
# {v1 name: model field name}
V1_FIELD_ALIASES = {
    "has_diversification_plan": "plan_diversification_en_place",
    "diversification_plan_actions": "plan_diversification_actions",
    "vegetarian_weekly_recurrence": "menu_vegetarien_frequence",
    "vegetarian_menu_type": "menu_vegetarien_type",
    "vegetarian_menu_bases": "menu_vegetarien_bases",
}
V1_FIELD_NAMES = {model_field_name: v1_name for v1_name, model_field_name in V1_FIELD_ALIASES.items()}
# same for the choice values renamed in French
# {v1 field name: {v1 value: model value}}
V1_CHOICE_VALUE_ALIASES = {
    "service_type": {
        "UNIQUE": Diagnostic.ServiceType.MENU_UNIQUE,
        "MULTIPLE_SELF": Diagnostic.ServiceType.CHOIX_MULTIPLE_LIBRE_SERVICE,
        "MULTIPLE_RESERVATION": Diagnostic.ServiceType.CHOIX_MULTIPLE_RESERVATION,
    },
    "vegetarian_weekly_recurrence": {
        "NEVER": Diagnostic.MenuVegetarienFrequence.JAMAIS,
        "LOW": Diagnostic.MenuVegetarienFrequence.MOINS_HEBDO,
        "MID": Diagnostic.MenuVegetarienFrequence.HEBDO,
        "HIGH": Diagnostic.MenuVegetarienFrequence.PLUS_HEBDO,
        "DAILY": Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
    },
    "diversification_plan_actions": {
        "PRODUCTS": Diagnostic.PlanDiversificationActions.PLATS_PRODUITS,
        "TRAINING": Diagnostic.PlanDiversificationActions.FORMATION,
    },
    "vegetarian_menu_bases": {
        "GRAIN": Diagnostic.MenuVegetarienBase.CEREALES_LEGUMINEUSES,
        "SOY": Diagnostic.MenuVegetarienBase.SOJA,
        "CHEESE": Diagnostic.MenuVegetarienBase.FROMAGE,
        "EGG": Diagnostic.MenuVegetarienBase.OEUFS,
        "READYMADE": Diagnostic.MenuVegetarienBase.PLATS_PRETS_A_L_EMPLOI,
    },
}
NON_APPRO_FIELDS_V1 = [V1_FIELD_NAMES.get(field_name, field_name) for field_name in Diagnostic.NON_APPRO_FIELDS]

FIELDS = (
    Diagnostic.META_FIELDS
    + Diagnostic.CANTEEN_FIELDS
    + Diagnostic.APPRO_FIELDS  # even the legacy ones
    + Diagnostic.APPRO_LOCAL_DEFINITION_FIELDS
    + NON_APPRO_FIELDS_V1
)
REQUIRED_FIELDS = ("year",)


def replace_choice_values(value, mapping):
    """
    Works for both simple choice fields & array (multiple choices) fields
    """
    if isinstance(value, list):
        return [mapping.get(item, item) for item in value]
    return mapping.get(value, value)


CREATE_ONLY_FIELDS = ("creation_source", *Diagnostic.MATOMO_FIELDS)
HIDDEN_FIELDS = CREATE_ONLY_FIELDS + ("generated_from_purchases", *Diagnostic.TUNNEL_PROGRESS_FIELDS)
READ_ONLY_FIELDS = (
    "id",
    "status",
    *Diagnostic.TELEDECLARATION_FIELDS,
    "generated_from_groupe_diagnostic",
    *Diagnostic.TELEDECLARATION_DATA_QUALITY_FIELDS,
    *Diagnostic.OTHER_COMPUTED_FIELDS,
)


class DiagnosticSerializer(serializers.ModelSerializer):
    is_teledeclared = serializers.BooleanField(read_only=True)  # property
    is_filled = serializers.BooleanField(read_only=True)

    v1_choice_value_aliases = V1_CHOICE_VALUE_ALIASES  # emptied in the v2 serializers

    def build_field(self, field_name, info, model_class, nested_depth):
        # v1 English names: build the field from the (French) model field
        if field_name in V1_FIELD_ALIASES:
            model_field_name = V1_FIELD_ALIASES[field_name]
            field_class, field_kwargs = super().build_field(model_field_name, info, model_class, nested_depth)
            field_kwargs["source"] = model_field_name
            return field_class, field_kwargs
        return super().build_field(field_name, info, model_class, nested_depth)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if (
            "total_leftovers" in representation
            and representation["total_leftovers"] is not None
            and representation["total_leftovers"] != ""
        ):
            representation["total_leftovers"] = representation["total_leftovers"] * 1000
        # v1 choice values: model value -> v1 value
        for field_name, value_aliases in self.v1_choice_value_aliases.items():
            if representation.get(field_name):
                model_to_v1_values = {model_value: v1_value for v1_value, model_value in value_aliases.items()}
                representation[field_name] = replace_choice_values(representation[field_name], model_to_v1_values)
        return representation

    def to_internal_value(self, data):
        # v1 choice values: v1 value -> model value
        if any(data.get(field_name) for field_name in self.v1_choice_value_aliases):
            data = data.copy()
            for field_name, value_aliases in self.v1_choice_value_aliases.items():
                if not data.get(field_name):
                    continue
                if hasattr(data, "getlist"):  # QueryDict (form data): a list field has several values
                    data.setlist(field_name, replace_choice_values(data.getlist(field_name), value_aliases))
                else:
                    data[field_name] = replace_choice_values(data[field_name], value_aliases)
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


class DiagnosticCheckSerializer(serializers.Serializer):
    is_empty = serializers.BooleanField(read_only=True)
    is_filled = serializers.BooleanField(read_only=True)
    is_clean = serializers.BooleanField(read_only=True)
    # infos = serializers.DictField(read_only=True)
    # warnings = serializers.DictField(read_only=True)
    errors = serializers.DictField(read_only=True)
    is_teledeclared = serializers.BooleanField(read_only=True)


class CentralKitchenDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    """
    This serializer masks financial data and gives the basic information on appro as percentages
    """

    class Meta:
        model = Diagnostic
        fields = FIELDS + Diagnostic.APPRO_PERCENTAGE_PROPERTY_FIELDS

    def to_representation(self, instance):
        """
        To facilitate the handling and merging of diagnostic in the front-end, we will include only appro
        fields if the central kitchen diagnostic is set to mode: APPRO
        This method pops non-appro fields if that is the case from the JSON representation
        """
        representation = super().to_representation(instance)
        if instance.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO:
            [representation.pop(field, "") for field in NON_APPRO_FIELDS_V1]
        if instance.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE:
            [representation.pop(field, "") for field in Diagnostic.COMPLETE_APPRO_FIELDS]
        return representation


class PublicDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = FIELDS + Diagnostic.APPRO_PERCENTAGE_PROPERTY_FIELDS


class PublicApproDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.APPRO_PERCENTAGE_PROPERTY_FIELDS


class PublicServiceDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + NON_APPRO_FIELDS_V1


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=HIDDEN_FIELDS)
class ManagerDiagnosticSerializer(DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = (
            FIELDS
            + Diagnostic.MATOMO_FIELDS
            + ["creation_source", "creation_date", "modification_date"]
            + Diagnostic.TUNNEL_PROGRESS_FIELDS
            + Diagnostic.TELEDECLARATION_FIELDS
            + Diagnostic.TELEDECLARATION_DATA_QUALITY_FIELDS
            + Diagnostic.OTHER_COMPUTED_FIELDS
            + [
                "generated_from_purchases",
                "status",
                "generated_from_groupe_diagnostic",
                "creation_source",
                "creation_date",
                "modification_date",
            ]
        )

    def get_fields(self):
        fields = super().get_fields()
        # some fields are required
        for field in REQUIRED_FIELDS:
            fields[field].required = True
            fields[field].allow_null = False
            fields[field].allow_blank = False
        # some fields are only available on create
        # and hidden from the docs (see extend_schema_serializer)
        for field in CREATE_ONLY_FIELDS:
            fields[field].write_only = True
            if self.instance is not None:
                fields.pop(field, None)
        # some fields are readonly
        for field in READ_ONLY_FIELDS:
            fields[field].read_only = True
        return fields


class FullDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    teledeclaration = ShortTeledeclarationSerializer(source="latest_submitted_teledeclaration")

    class Meta:
        model = Diagnostic
        fields = (
            FIELDS
            + ["teledeclaration"]
            + Diagnostic.TELEDECLARATION_FIELDS
            + Diagnostic.CREATION_META_FIELDS
            + Diagnostic.TUNNEL_PROGRESS_FIELDS
        )


class SimpleTeledeclarationDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = (
            Diagnostic.META_FIELDS
            + Diagnostic.SIMPLE_APPRO_FIELDS
            + Diagnostic.APPRO_LOCAL_DEFINITION_FIELDS
            + NON_APPRO_FIELDS_V1
        )


class CompleteTeledeclarationDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = (
            Diagnostic.META_FIELDS
            + Diagnostic.COMPLETE_APPRO_FIELDS
            + Diagnostic.APPRO_LOCAL_DEFINITION_FIELDS
            + NON_APPRO_FIELDS_V1
        )


class ApproDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.APPRO_PERCENTAGE_PROPERTY_FIELDS


class ApproDeferredTeledeclarationDiagnosticSerializer(ReadOnlySerializerMixin, DiagnosticSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + NON_APPRO_FIELDS_V1


class SimpleApproOnlyTeledeclarationDiagnosticSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.SIMPLE_APPRO_FIELDS + Diagnostic.APPRO_LOCAL_DEFINITION_FIELDS


class CompleteApproOnlyTeledeclarationDiagnosticSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.META_FIELDS + Diagnostic.COMPLETE_APPRO_FIELDS + Diagnostic.APPRO_LOCAL_DEFINITION_FIELDS


class DiagnosticAndCanteenSerializer(FullDiagnosticSerializer):
    canteen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Diagnostic
        fields = tuple(FullDiagnosticSerializer().fields) + ("canteen",)

    def get_canteen(self, obj):
        from .canteen import FullCanteenSerializer

        return FullCanteenSerializer(obj.canteen).data


class DiagnosticApproStatsSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = Diagnostic.APPRO_STATS_FIELDS


class DiagnosticRecapSerializer(ReadOnlySerializerMixin, serializers.Serializer):
    year = serializers.IntegerField()
    is_teledeclared = serializers.BooleanField()
    declaration_donnees = serializers.JSONField()
    canteen_diagnostic_id = serializers.IntegerField(source="canteen_diagnostic.id", allow_null=True)
    canteen_diagnostic_appro_stats = DiagnosticApproStatsSerializer(source="canteen_diagnostic")
    generated_from_groupe_diagnostic_id = serializers.IntegerField(
        source="generated_from_groupe_diagnostic.id", allow_null=True
    )
    generated_from_groupe_diagnostic_mode = serializers.CharField(
        source="generated_from_groupe_diagnostic.central_kitchen_diagnostic_mode", allow_null=True
    )
    generated_from_groupe_diagnostic_appro_stats = DiagnosticApproStatsSerializer(
        source="generated_from_groupe_diagnostic"
    )
    notes = serializers.DictField()
