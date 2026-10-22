from rest_framework import serializers

from api.serializers.utils import ReadOnlySerializerMixin
from data.models import Canteen, Diagnostic


class DiagnosticTeledeclaredOpenDataSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(source="teledeclaration_id")
    diagnostic_type = serializers.CharField(source="teledeclaration_type")  # TODO: avoid renaming?
    creation_date = serializers.DateTimeField(source="teledeclaration_date")
    version = serializers.CharField(source="teledeclaration_version")

    canteen_name = serializers.CharField(source="canteen_snapshot.name")
    canteen_siret = serializers.CharField(source="canteen_snapshot.siret")
    canteen_siren_unite_legale = serializers.CharField(source="canteen_snapshot.siren_unite_legale")
    canteen_central_kitchen_siret = serializers.CharField(
        source="canteen_snapshot.central_producer_siret"
    )  # incohérence dans le nom du champ
    canteen_city_insee_code = serializers.CharField(source="canteen_snapshot.city_insee_code")
    canteen_epci = serializers.CharField(source="canteen_snapshot.epci")
    canteen_epci_lib = serializers.CharField(source="canteen_snapshot.epci_lib")
    canteen_pat_list = serializers.SerializerMethodField()
    canteen_pat_lib_list = serializers.SerializerMethodField()
    canteen_department = serializers.CharField(source="canteen_snapshot.department")
    canteen_department_lib = serializers.CharField(source="canteen_snapshot.department_lib")
    canteen_region = serializers.CharField(source="canteen_snapshot.region")
    canteen_region_lib = serializers.CharField(source="canteen_snapshot.region_lib")
    canteen_economic_model = serializers.CharField(source="canteen_snapshot.economic_model")
    canteen_management_type = serializers.CharField(source="canteen_snapshot.management_type")
    canteen_production_type = serializers.CharField(source="canteen_snapshot.production_type")
    canteen_sector_list = serializers.SerializerMethodField()
    canteen_line_ministry = serializers.SerializerMethodField()

    teledeclaration_ratio_bio = serializers.SerializerMethodField()  # TODO: compute & store in DB?
    teledeclaration_ratio_egalim_hors_bio = serializers.SerializerMethodField(
        read_only=True
    )  # TODO: compute & store in DB?

    class Meta:
        model = Diagnostic
        fields = (
            # diagnostic fields
            "id",  # teledeclaration_id
            "diagnostic_type",  # teledeclaration_type
            "teledeclaration_mode",
            "creation_date",  # teledeclaration_date
            "year",
            "version",
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
            "canteen_pat_list",
            "canteen_pat_lib_list",
            "canteen_department",
            "canteen_department_lib",
            "canteen_region",
            "canteen_region_lib",
            "canteen_economic_model",
            "canteen_management_type",
            "canteen_production_type",
            "canteen_sector_list",
            "canteen_line_ministry",
            # value fields
            "teledeclaration_ratio_bio",
            "teledeclaration_ratio_egalim_hors_bio",
        )

    def get_canteen_pat_list(self, obj):
        return ",".join(obj.canteen_snapshot.get("pat_list", []) or [])

    def get_canteen_pat_lib_list(self, obj):
        return ",".join(obj.canteen_snapshot.get("pat_lib_list", []) or [])

    def get_canteen_sector_list(self, obj):
        return ",".join(obj.canteen_snapshot_sector_lib_list or [])

    def get_canteen_line_ministry(self, obj):
        line_ministry = obj.canteen_snapshot.get("line_ministry", None)
        if line_ministry and line_ministry not in ["autre"]:
            return Canteen.Ministries(line_ministry).label
        return None

    def get_teledeclaration_ratio_bio(self, obj):
        if obj.pourcentage_bio:
            return obj.pourcentage_bio / 100

    def get_teledeclaration_ratio_egalim_hors_bio(self, obj):
        if obj.pourcentage_egalim_hors_bio:
            return obj.pourcentage_egalim_hors_bio / 100
