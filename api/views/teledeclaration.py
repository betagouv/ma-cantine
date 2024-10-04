import logging
import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from xhtml2pdf import pisa

from api.permissions import IsAuthenticatedOrTokenHasResourceScope
from api.serializers import FullDiagnosticSerializer
from data.models import Canteen, Diagnostic, Teledeclaration

from .utils import camelize

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        summary="Télédéclarer un diagnostic",
        description="La télédéclaration créée prendra le diagnostic de l'année concernée pour créer un snapshot immutable. En créant une télédéclaration,"
        + "l'utilisateur s'engage sur l'honneur sur la véracité des données télédéclarées.\n\n"
        + "C'est possible d'envoyer une liste de `diagnostic_ids` pour télédéclarer plusieurs avec une requête. Dans ce cas, vous recevrez une `200` réponse, sinon une `201`.",
    ),
)
class TeledeclarationCreateView(APIView):
    """
    This view allows creating a teledeclaration from an
    existing diagnostic.
    """

    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    @extend_schema(
        request=inline_serializer(name="Testing", fields={"diagnostic_id": serializers.IntegerField()}),
        responses={
            "201": FullDiagnosticSerializer,
        },
    )
    def post(self, request):
        data = request.data
        diagnostic_id = data.get("diagnostic_id")
        if not diagnostic_id:
            raise ValidationError("diagnosticId manquant")
        if not settings.ENABLE_TELEDECLARATION:
            raise PermissionDenied("La campagne de télédéclaration n'est pas ouverte.")

        td = TeledeclarationCreateView._teledeclare_diagnostic(diagnostic_id, request.user)
        data = FullDiagnosticSerializer(td.diagnostic).data
        return JsonResponse(camelize(data), status=status.HTTP_201_CREATED)

    def _teledeclare_diagnostic(diagnostic_id, user):
        try:
            diagnostic = Diagnostic.objects.get(pk=diagnostic_id)
        except Diagnostic.DoesNotExist:
            raise PermissionDenied()  # in general we throw 403s not 404s

        if user not in diagnostic.canteen.managers.all():
            raise PermissionDenied()

        try:
            Teledeclaration.validate_diagnostic(diagnostic)
        except DjangoValidationError as e:
            raise TeledeclarationCreateView._parse_diagnostic_validation_error(e) from e

        try:
            td = Teledeclaration.create_from_diagnostic(diagnostic, user)
            return td
        except DjangoValidationError as e:
            if hasattr(e, "message") and e.message == "Données d'approvisionnement manquantes":
                message = e.message
            else:
                message = "Il existe déjà une télédéclaration en cours pour cette année"
            raise ValidationError(message) from e

    def _parse_diagnostic_validation_error(e):
        if hasattr(e, "message"):
            return ValidationError(e.message)
        elif hasattr(e, "messages"):
            return ValidationError(e.messages[0])
        else:
            logger.error(f"Unhandled validation error when teledeclaring: {e}")
            return ValidationError("Unknown error")


@extend_schema_view(
    post=extend_schema(
        summary="Annuler une télédéclaration existante.",
        description="Un diagnostic ne peut pas être modifié si une télédéclaration a été créée. Pour corriger des données, l'utilisateur devra d'abord annuler la télédeclaration. À noter que l'utilisateur devra en créer une nouvelle une fois que le diagnostic a été corrigé.",
    ),
)
class TeledeclarationCancelView(APIView):
    """
    This view cancels a submitted teledeclaration
    """

    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def post(self, request, *args, **kwargs):
        try:
            if not settings.ENABLE_TELEDECLARATION:
                raise PermissionDenied("La campagne de télédéclaration n'est pas ouverte.")

            teledeclaration_id = kwargs.get("pk")
            teledeclaration = Teledeclaration.objects.get(pk=teledeclaration_id)

            acceptedYear = datetime.now().year - 1
            if teledeclaration.year != acceptedYear:
                raise PermissionDenied(
                    f"Seules les télédéclarations pour l'année {acceptedYear} peuvent être annulées"
                )

            if request.user not in teledeclaration.canteen.managers.all():
                raise PermissionDenied()

            teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
            teledeclaration.save()

            data = FullDiagnosticSerializer(teledeclaration.diagnostic).data
            return JsonResponse(camelize(data), status=status.HTTP_200_OK)

        except Teledeclaration.DoesNotExist:
            raise ValidationError("La télédéclaration specifiée n'existe pas")


@extend_schema_view(
    get=extend_schema(
        summary="Obtenir une représentation PDF de la télédéclaration.",
        description="",
    ),
)
class TeledeclarationPdfView(APIView):
    """
    This view returns a PDF for proof of teledeclaration
    """

    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def get(self, request, *args, **kwargs):
        teledeclaration_id = kwargs.get("pk")
        if not teledeclaration_id:
            raise ValidationError("teledeclarationId manquant")

        try:
            teledeclaration = Teledeclaration.objects.get(pk=teledeclaration_id)
        except Teledeclaration.DoesNotExist:
            raise ValidationError("La télédéclaration specifiée n'existe pas")

        if request.user not in teledeclaration.canteen.managers.all():
            raise PermissionDenied()

        if teledeclaration.status != Teledeclaration.TeledeclarationStatus.SUBMITTED:
            raise ValidationError("La télédéclaration n'est pas validée par l'utilisateur")

        template = (
            get_template("teledeclaration_campaign_2024/index.html")
            if teledeclaration.year >= 2023
            else get_template("teledeclaration_pdf.html")
        )
        context = TeledeclarationPdfView.get_context(teledeclaration)
        html = template.render(context)

        response = HttpResponse(content_type="application/pdf")
        filename = TeledeclarationPdfView.get_filename(teledeclaration)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=TeledeclarationPdfView.link_callback)

        if pisa_status.err:
            logger.error(f"Error while generating PDF for teledeclaration {teledeclaration.id}:\n{pisa_status.err}")
            return HttpResponse("An error ocurred", status=500)

        return response

    @staticmethod
    def get_context(teledeclaration):
        declared_data = teledeclaration.declared_data

        central_kitchen_siret = declared_data.get("central_kitchen_siret", None)
        central_kitchen_name = None
        if teledeclaration.teledeclaration_mode == Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO:
            try:
                central_kitchen_name = Canteen.objects.get(siret=central_kitchen_siret).name
            except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned):
                pass

        canteen_data = declared_data["canteen"]
        teledeclaration_data = declared_data["teledeclaration"]
        processed_canteen_data = TeledeclarationPdfView._get_canteen_override_data(canteen_data)
        processed_diagnostic_data = TeledeclarationPdfView._get_teledeclaration_override_data(teledeclaration_data)
        additional_questions = TeledeclarationPdfView._get_applicable_diagnostic_rules(canteen_data)

        is_complete = (
            declared_data["teledeclaration"].get("diagnostic_type", None) == Diagnostic.DiagnosticType.COMPLETE
        )
        structure_complete_appro_data = {}
        if is_complete:
            structure_complete_appro_data = TeledeclarationPdfView._structure_complete_appro_data(teledeclaration_data)

        return {
            **{**teledeclaration_data, **processed_diagnostic_data},
            **{
                "diagnostic_type": "complète" if is_complete else "simplifiée",
                "year": teledeclaration.year,
                "date": teledeclaration.creation_date,
                "applicant": declared_data["applicant"]["name"],
                "teledeclaration_mode": teledeclaration.teledeclaration_mode,
                "central_kitchen_siret": central_kitchen_siret,
                "central_kitchen_name": central_kitchen_name,
                "satellites": declared_data.get("satellites", []),
                "canteen": {**canteen_data, **processed_canteen_data},
                "additional_questions": additional_questions,
                "complete_appro": structure_complete_appro_data,
            },
        }

    @staticmethod
    def get_filename(teledeclaration):
        year = teledeclaration.year
        canteenName = slugify(teledeclaration.declared_data["canteen"]["name"])
        creation_date = teledeclaration.creation_date.strftime("%Y-%m-%d")
        return f"teledeclaration-{year}--{canteenName}--{creation_date}.pdf"

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
    def _get_canteen_override_data(canteen_data):
        """
        Returns the JSON data of the canteen parameters that need to be overriden in order for
        them to be human-readable (e.g., replacing keys with labels)
        """
        return {
            "sectors": ", ".join([x["name"] for x in (canteen_data.get("sectors") or [])]),
            "production_type": (
                Canteen.ProductionType(canteen_data["production_type"]).label
                if canteen_data.get("production_type")
                else None
            ),
            "management_type": (
                Canteen.ManagementType(canteen_data["management_type"]).label
                if canteen_data.get("management_type")
                else None
            ),
            "line_ministry": (
                Canteen.Ministries(canteen_data["line_ministry"]).label if canteen_data.get("line_ministry") else None
            ),
            "economic_model": (
                Canteen.EconomicModel(canteen_data["economic_model"]).label
                if canteen_data.get("economic_model")
                else None
            ),
        }

    @staticmethod
    def _get_teledeclaration_override_data(teledeclaration_data):
        """
        Returns the JSON data of the teledeclaration parameters that need to be overriden in order for
        them to be human-readable (e.g., replacing keys with labels and merging multiple choice with
        "other" editable choices)
        """
        processed_waste_actions = [
            Diagnostic.WasteActions(x).label for x in (teledeclaration_data.get("waste_actions") or [])
        ]
        combined_waste_actions = processed_waste_actions + (
            [teledeclaration_data.get("other_waste_action")] if teledeclaration_data.get("other_waste_action") else []
        )
        processed_communication_supports = [
            Diagnostic.CommunicationType(x).label for x in (teledeclaration_data.get("communication_supports") or [])
        ]
        combined_communication_supports = processed_communication_supports + (
            [teledeclaration_data.get("other_communication_support")]
            if teledeclaration_data.get("other_communication_support")
            else []
        )

        return {
            "waste_actions": combined_waste_actions,
            "diversification_plan_actions": [
                Diagnostic.DiversificationPlanActions(x).label
                for x in (teledeclaration_data.get("diversification_plan_actions") or [])
            ],
            "vegetarian_weekly_recurrence": (
                Diagnostic.MenuFrequency(teledeclaration_data["vegetarian_weekly_recurrence"]).label
                if teledeclaration_data.get("vegetarian_weekly_recurrence")
                else None
            ),
            "vegetarian_menu_type": (
                Diagnostic.MenuType(teledeclaration_data["vegetarian_menu_type"]).label
                if teledeclaration_data.get("vegetarian_menu_type")
                else None
            ),
            "vegetarian_menu_bases": [
                Diagnostic.VegetarianMenuBase(x).label
                for x in (teledeclaration_data.get("vegetarian_menu_bases") or [])
            ],
            "communication_frequency": (
                Diagnostic.CommunicationFrequency(teledeclaration_data["communication_frequency"]).label
                if teledeclaration_data.get("communication_frequency")
                else None
            ),
            "communication_supports": combined_communication_supports,
        }

    # this method should correspond to the rules in frontend utils : applicableDiagnosticRules
    @staticmethod
    def _get_applicable_diagnostic_rules(canteen_data):
        donation_agreement = diversification_plan = False
        if "daily_meal_count" in canteen_data and canteen_data["daily_meal_count"]:
            donation_agreement = canteen_data["daily_meal_count"] >= 3000
            diversification_plan = canteen_data["daily_meal_count"] >= 200
        return {
            "donation_agreement": donation_agreement,
            "diversification_plan": diversification_plan,
        }

    @staticmethod
    def _structure_complete_appro_data(teledeclaration_data):
        """
        This function restructures appro data to reduce template code
        """
        labels_variable_to_display = {
            "bio": "Bio",
            "label_rouge": "Label Rouge",
            "aocaop_igp_stg": "AOC/AOP, IGP ou STG",
            "hve": "Certification Environnementale de Niveau 2 ou HVE",
            "peche_durable": "Écolabel pêche durable",
            "rup": "RUP",
            "commerce_equitable": "Commerce Équitable",
            "fermier": "Fermier",
            "externalites": "Externalités environnementales",
            "performance": "Performance environnementale",
            "non_egalim": "non-EGAlim",
            "france": "provenance France",
            "short_distribution": "circuit-court",
            "local": "« local »",
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
                structured_data[display_label][display_family] = teledeclaration_data[f"value_{family}_{label}"]
        return structured_data
