import logging
import os

from django_filters import rest_framework as django_filters
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.views import APIView
from xhtml2pdf import pisa

from api.permissions import (
    IsAuthenticatedOrTokenHasResourceScope,
    IsAuthenticated,
    IsLinkedCanteenManager,
    IsCanteenManager,
)
from api.serializers import DiagnosticTeledeclaredAnalysisSerializer, DiagnosticTeledeclaredOpenDataSerializer
from data.models import Canteen, Diagnostic, Teledeclaration
from macantine.utils import CAMPAIGN_DATES


logger = logging.getLogger(__name__)


class DiagnosticTeledeclarationCreateView(APIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    required_scopes = ["canteen"]

    def post(self, request, *args, **kwargs):
        canteen = get_object_or_404(Canteen, pk=kwargs.get("canteen_pk"))
        if not IsCanteenManager().has_object_permission(self.request, self, canteen):
            raise PermissionDenied()
        diagnostic = get_object_or_404(Diagnostic, pk=kwargs.get("pk"))

        # if ValidationError, it will be raised (and handled by custom_exception_handler)
        diagnostic.teledeclare(request.user)

        return HttpResponse(status=200)


class DiagnosticTeledeclarationCancelView(APIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    required_scopes = ["canteen"]

    def post(self, request, *args, **kwargs):
        canteen = get_object_or_404(Canteen, pk=kwargs.get("canteen_pk"))
        if not IsCanteenManager().has_object_permission(self.request, self, canteen):
            raise PermissionDenied()
        diagnostic = get_object_or_404(Diagnostic, pk=kwargs.get("pk"))

        # if ValidationError, it will be raised (and handled by custom_exception_handler)
        diagnostic.cancel()

        return HttpResponse(status=200)


@extend_schema_view(
    get=extend_schema(summary="Obtenir une représentation PDF de la télédéclaration.", tags=["teledeclaration"]),
)
class DiagnosticTeledeclarationPdfView(APIView):
    """
    This view returns a PDF for proof of teledeclaration
    """

    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsLinkedCanteenManager]
    required_scopes = ["teledeclaration"]

    def get(self, request, *args, **kwargs):
        canteen = get_object_or_404(Canteen, pk=kwargs.get("canteen_pk"))
        if not IsCanteenManager().has_object_permission(self.request, self, canteen):
            raise PermissionDenied()
        diagnostic = get_object_or_404(Diagnostic, pk=kwargs.get("pk"))

        if not diagnostic.is_teledeclared:
            raise ValidationError("Le diagnostic n'a pas été télédéclaré.")

        template = (
            get_template("teledeclaration_campaign_2024/index.html")
            if diagnostic.year >= 2023
            else get_template("teledeclaration_pdf.html")
        )
        context = DiagnosticTeledeclarationPdfView.get_context(diagnostic)
        html = template.render(context)

        response = HttpResponse(content_type="application/pdf")
        filename = DiagnosticTeledeclarationPdfView.get_filename(diagnostic)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=DiagnosticTeledeclarationPdfView.link_callback)

        if pisa_status.err:
            logger.error(f"Error while generating PDF for diagnostic {diagnostic.id}:\n{pisa_status.err}")
            return HttpResponse("An error ocurred", status=500)

        return response

    @staticmethod
    def get_context(diagnostic):
        central_kitchen_siret = diagnostic.canteen_snapshot.get("central_kitchen_siret", None)
        central_kitchen_name = None
        if diagnostic.teledeclaration_mode == Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO:
            try:
                central_kitchen_name = Canteen.objects.get(siret=central_kitchen_siret).name
            except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned):
                pass

        canteen_snapshot = diagnostic.canteen_snapshot
        processed_canteen_snapshot = DiagnosticTeledeclarationPdfView._get_canteen_override_data(diagnostic)
        processed_diagnostic_data = DiagnosticTeledeclarationPdfView._get_teledeclaration_override_data(diagnostic)
        additional_questions = DiagnosticTeledeclarationPdfView._get_applicable_diagnostic_rules(canteen_snapshot)

        structure_complete_appro_data = {}
        if diagnostic.is_diagnostic_type_complete:
            structure_complete_appro_data = DiagnosticTeledeclarationPdfView._structure_complete_appro_data(diagnostic)

        return {
            **diagnostic.__dict__,
            **processed_diagnostic_data,
            **{
                "diagnostic_type": "détaillée" if diagnostic.is_diagnostic_type_complete else "simplifiée",
                "year": diagnostic.year,
                "date": diagnostic.teledeclaration_date,
                "applicant": diagnostic.applicant_snapshot["name"],
                "teledeclaration_mode": diagnostic.teledeclaration_mode,
                "central_kitchen_siret": central_kitchen_siret,
                "central_kitchen_name": central_kitchen_name,
                "satellites": diagnostic.satellites_snapshot or [],
                "canteen": {**canteen_snapshot, **processed_canteen_snapshot},
                "additional_questions": additional_questions,
                "complete_appro": structure_complete_appro_data,
            },
        }

    @staticmethod
    def get_filename(diagnostic):
        year = diagnostic.year
        canteen_name = slugify(diagnostic.canteen_snapshot["name"])
        teledeclaration_date = diagnostic.teledeclaration_date.strftime("%Y-%m-%d")
        return f"teledeclaration-{year}--{canteen_name}--{teledeclaration_date}.pdf"

    @staticmethod
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        https://xhtml2pdf.readthedocs.io/en/latest/usage.html#using-xhtml2pdf-in-django
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL
            sRoot = settings.STATIC_ROOT
            mUrl = settings.MEDIA_URL
            mRoot = settings.MEDIA_ROOT

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception("media URI must start with {} or {}".format(sUrl, mUrl))
        return path

    @staticmethod
    def _get_canteen_override_data(diagnostic):
        """
        Returns the JSON data of the canteen parameters that need to be overriden in order for
        them to be human-readable (e.g., replacing keys with labels)
        """
        return {
            "sectors": diagnostic.canteen_snapshot_sector_list_display,
            "production_type": (
                Canteen.ProductionType(diagnostic.canteen_snapshot["production_type"]).label
                if diagnostic.canteen_snapshot.get("production_type")
                else None
            ),
            "management_type": (
                Canteen.ManagementType(diagnostic.canteen_snapshot["management_type"]).label
                if diagnostic.canteen_snapshot.get("management_type")
                else None
            ),
            "line_ministry": (
                Canteen.Ministries(diagnostic.canteen_snapshot["line_ministry"]).label
                if diagnostic.canteen_snapshot.get("line_ministry")
                else None
            ),
            "economic_model": (
                Canteen.EconomicModel(diagnostic.canteen_snapshot["economic_model"]).label
                if diagnostic.canteen_snapshot.get("economic_model")
                else None
            ),
        }

    @staticmethod
    def _get_teledeclaration_override_data(diagnostic):
        """
        Returns the JSON data of the teledeclaration parameters that need to be overriden in order for
        them to be human-readable (e.g., replacing keys with labels and merging multiple choice with
        "other" editable choices)
        """
        processed_waste_actions = [Diagnostic.WasteActions(x).label for x in (diagnostic.waste_actions or [])]
        combined_waste_actions = processed_waste_actions + (
            [diagnostic.other_waste_action] if diagnostic.other_waste_action else []
        )
        processed_communication_supports = [
            Diagnostic.CommunicationType(x).label for x in (diagnostic.communication_supports or [])
        ]
        combined_communication_supports = processed_communication_supports + (
            [diagnostic.other_communication_support] if diagnostic.other_communication_support else []
        )

        return {
            "waste_actions": combined_waste_actions,
            "diversification_plan_actions": [
                Diagnostic.DiversificationPlanActions(x).label for x in (diagnostic.diversification_plan_actions or [])
            ],
            "vegetarian_weekly_recurrence": (
                Diagnostic.VegetarianMenuFrequency(diagnostic.vegetarian_weekly_recurrence).label
                if diagnostic.vegetarian_weekly_recurrence
                else None
            ),
            "service_type": (
                Diagnostic.ServiceType(diagnostic.service_type).label if diagnostic.service_type else None
            ),
            "vegetarian_menu_type": (
                Diagnostic.VegetarianMenuType(diagnostic.vegetarian_menu_type).label
                if diagnostic.vegetarian_menu_type
                else None
            ),
            "vegetarian_menu_bases": [
                Diagnostic.VegetarianMenuBase(x).label for x in (diagnostic.vegetarian_menu_bases or [])
            ],
            "communication_frequency": (
                Diagnostic.CommunicationFrequency(diagnostic.communication_frequency).label
                if diagnostic.communication_frequency
                else None
            ),
            "communication_supports": combined_communication_supports,
        }

    # this method should correspond to the rules in frontend utils : applicableDiagnosticRules
    @staticmethod
    def _get_applicable_diagnostic_rules(canteen_snapshot):
        donation_agreement = diversification_plan = False
        if "daily_meal_count" in canteen_snapshot and canteen_snapshot["daily_meal_count"]:
            donation_agreement = canteen_snapshot["daily_meal_count"] >= 3000
            diversification_plan = canteen_snapshot["daily_meal_count"] >= 200
        return {
            "donation_agreement": donation_agreement,
            "diversification_plan": diversification_plan,
        }

    @staticmethod
    def _structure_complete_appro_data(diagnostic):
        """
        This function restructures appro data to reduce template code
        """
        labels_variable_to_display = {
            "bio": "Bio",
            "bio_dont_commerce_equitable": "Bio et Commerce équitable",
            "label_rouge": "Label Rouge",
            "aocaop_igp_stg": "AOC/AOP, IGP ou STG",
            "hve": "Certification Environnementale de Niveau 2 ou HVE",
            "peche_durable": "Écolabel pêche durable",
            "rup": "RUP",
            "commerce_equitable": "Commerce équitable (hors bio)",
            "fermier": "Fermier",
            "externalites": "Externalités environnementales",
            "performance": "Performance environnementale",
            "non_egalim": "Non-EGalim",
            "france": "Origine France",
            "circuit_court": "Origine France : dont circuit-court",
            "local": "Origine France : dont local",
        }
        family_variable_to_display = {
            "viandes_volailles": "Viandes et volailles",
            "produits_de_la_mer": "Poissons, produits de la mer et de l'aquaculture",
            "fruits_et_legumes": "Fruits et légumes",
            "charcuterie": "Charcuterie",
            "produits_laitiers": "Produits laitiers",
            "boulangerie": "Boulangerie",
            "boissons": "Boissons",
            "autres": "Autres produits",
        }
        structured_data = {}
        for label, display_label in labels_variable_to_display.items():
            structured_data[display_label] = {}
            for family, display_family in family_variable_to_display.items():
                structured_data[display_label][display_family] = getattr(diagnostic, f"valeur_{family}_{label}")
        return structured_data


class DiagnosticTeledeclaredAnalysisListView(ListAPIView):
    serializer_class = DiagnosticTeledeclaredAnalysisSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    ordering_fields = ["creation_date"]

    def get_queryset(self):
        return Diagnostic.objects.with_meal_price().historical_valid_td(CAMPAIGN_DATES.keys())


class DiagnosticTeledeclaredOpenDataListView(ListAPIView):
    serializer_class = DiagnosticTeledeclaredOpenDataSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    ordering_fields = ["creation_date"]

    def get_queryset(self, year):
        return Diagnostic.objects.publicly_visible().valid_td_by_year(year).order_by("teledeclaration_date")
