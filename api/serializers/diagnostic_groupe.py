from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from data.models import Canteen


class DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer(serializers.ModelSerializer):
    """
    A satellite of the groupe, with its nombre_repas_an (stored in the groupe's Diagnostic)
    - context["satellites_nombre_repas_an"]: the Diagnostic.satellites_nombre_repas_an dict
    """

    nombre_repas_an = serializers.SerializerMethodField()

    class Meta:
        model = Canteen
        fields = (
            "id",
            "siret",
            "siren_unite_legale",
            "name",
            "nombre_repas_an",
        )
        read_only_fields = fields

    def get_nombre_repas_an(self, obj) -> int | None:
        satellites_nombre_repas_an = self.context.get("satellites_nombre_repas_an") or {}
        return satellites_nombre_repas_an.get(str(obj.id))


class DiagnosticGroupeCouvertsAnnuelsUpdateSerializer(serializers.Serializer):
    """
    Update the nombre_repas_an of one satellite of the groupe
    """

    id = serializers.IntegerField(help_text="id de la cantine satellite")
    nombre_repas_an = serializers.IntegerField(
        allow_null=True, min_value=0, max_value=999999999, help_text="nombre de repas par an du satellite"
    )


def get_satellites_nombre_repas_an_list(diagnostic) -> list | None:
    """
    The satellites of the groupe, with their nombre_repas_an (None if the diagnostic's canteen is not a groupe)
    """
    if not diagnostic.canteen or not diagnostic.canteen.is_groupe:
        return None
    return DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer(
        diagnostic.canteen.satellites.order_by("name"),
        many=True,
        context={"satellites_nombre_repas_an": diagnostic.satellites_nombre_repas_an},
    ).data


@extend_schema_field(DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer(many=True, allow_null=True))
class SatellitesNombreRepasAnField(serializers.Field):
    """
    Read-only: the satellites of the groupe, with their nombre_repas_an
    - to edit them: see the groupe-couverts-annuels endpoint
    """

    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        kwargs.setdefault("help_text", "Groupe : nombre de repas par an de chaque satellite (lecture seule)")
        super().__init__(**kwargs)

    def to_representation(self, value):
        return get_satellites_nombre_repas_an_list(value)
