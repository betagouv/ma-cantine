from drf_spectacular.utils import extend_schema_serializer

from api.serializers.diagnostic import DiagnosticSerializer
from api.serializers.utils import set_help_text_from_verbose_name
from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_all_years,
)

CREATE_ONLY_FIELDS = ("creation_source", *Diagnostic.MATOMO_FIELDS)
READ_ONLY_FIELDS = (
    "id",
    "canteen_id",
    "status",
    "is_teledeclared",
    "is_filled",
    "generated_from_groupe_diagnostic",
    *Diagnostic.TELEDECLARATION_FIELDS,
    "creation_date",
    "modification_date",
)

VOLET_META_FIELDS = [
    "id",
    "canteen_id",
    "year",
    "central_kitchen_diagnostic_mode",
    "is_teledeclared",
    "is_filled",
]


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=CREATE_ONLY_FIELDS)
class DiagnosticV2Serializer(DiagnosticSerializer):
    """
    The diagnostic itself, without the volets (each volet has its own serializer)
    """

    class Meta:
        model = Diagnostic
        fields = (
            "id",
            "canteen_id",
            "year",
            "central_kitchen_diagnostic_mode",
            "status",
            "is_teledeclared",
            "is_filled",
            "generated_from_groupe_diagnostic",
            *Diagnostic.TELEDECLARATION_FIELDS,
            "creation_date",
            "modification_date",
            *CREATE_ONLY_FIELDS,
        )

    def get_fields(self):
        fields = super().get_fields()
        fields["year"].required = True
        fields["year"].allow_null = False
        # some fields are only available on create
        # and hidden from the docs (see extend_schema_serializer)
        for field in CREATE_ONLY_FIELDS:
            fields[field].write_only = True
            if self.instance is not None:
                fields.pop(field, None)
        # the year cannot be changed once the diagnostic is created
        if self.instance is not None:
            fields["year"].read_only = True
        for field in READ_ONLY_FIELDS:
            fields[field].read_only = True
        return fields


class BaseDiagnosticVoletV2Serializer(DiagnosticSerializer):
    """
    A volet of the diagnostic: its fields depend on the diagnostic's year (see TELEDECLARATION_FIELDS)
    - Meta.fields contains the volet's fields of all the years
    - get_fields() only keeps the ones of the diagnostic's year
    """

    volet = None  # TELEDECLARATION_FIELDS key
    extra_read_only_fields = []  # volet fields that are not in TELEDECLARATION_FIELDS (ex: computed stats)

    def get_diagnostic_type(self):
        return None

    def get_year_volet_fields(self):
        try:
            return get_teledeclaration_fields_all(self.instance.year, self.volet, self.get_diagnostic_type())
        except ValueError:
            return []

    def get_fields(self):
        fields = super().get_fields()
        for field in VOLET_META_FIELDS + self.extra_read_only_fields:
            fields[field].read_only = True
        # no instance: the docs (all the years)
        if isinstance(self.instance, Diagnostic):
            year_volet_fields = self.get_year_volet_fields()
            for field in get_teledeclaration_fields_all_years(self.volet):
                if field not in year_volet_fields:
                    fields.pop(field, None)
        return fields


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=("tunnel_appro", "generated_from_purchases"))
class DiagnosticVoletApprovisionnementV2Serializer(BaseDiagnosticVoletV2Serializer):
    volet = "APPROVISIONNEMENT"
    extra_read_only_fields = Diagnostic.APPRO_STATS_FIELDS

    class Meta:
        model = Diagnostic
        fields = (
            VOLET_META_FIELDS
            + ["diagnostic_type"]
            + get_teledeclaration_fields_all_years("APPROVISIONNEMENT")
            + Diagnostic.APPRO_STATS_FIELDS
            + ["tunnel_appro", "generated_from_purchases"]
        )

    def get_diagnostic_type(self):
        # the fields depend on the diagnostic_type: use the new one if it is being updated
        return getattr(self, "initial_data", {}).get("diagnostic_type", self.instance.diagnostic_type)


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=("tunnel_waste",))
class DiagnosticVoletGaspillageV2Serializer(BaseDiagnosticVoletV2Serializer):
    volet = "GASPILLAGE"

    class Meta:
        model = Diagnostic
        fields = VOLET_META_FIELDS + get_teledeclaration_fields_all_years("GASPILLAGE") + ["tunnel_waste"]


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=("tunnel_diversification",))
class DiagnosticVoletDiversificationV2Serializer(BaseDiagnosticVoletV2Serializer):
    volet = "DIVERSIFICATION"

    class Meta:
        model = Diagnostic
        fields = (
            VOLET_META_FIELDS + get_teledeclaration_fields_all_years("DIVERSIFICATION") + ["tunnel_diversification"]
        )


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=("tunnel_plastic",))
class DiagnosticVoletPlastiqueV2Serializer(BaseDiagnosticVoletV2Serializer):
    volet = "PLASTIQUE"

    class Meta:
        model = Diagnostic
        fields = VOLET_META_FIELDS + get_teledeclaration_fields_all_years("PLASTIQUE") + ["tunnel_plastic"]


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=("tunnel_info",))
class DiagnosticVoletInformationV2Serializer(BaseDiagnosticVoletV2Serializer):
    volet = "INFORMATION"

    class Meta:
        model = Diagnostic
        fields = VOLET_META_FIELDS + get_teledeclaration_fields_all_years("INFORMATION") + ["tunnel_info"]
