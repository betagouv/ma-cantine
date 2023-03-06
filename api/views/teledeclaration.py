import logging
import os
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError as DjangoValidationError
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from xhtml2pdf import pisa
from data.models import Diagnostic, Teledeclaration, Canteen
from api.serializers import FullDiagnosticSerializer
from api.permissions import IsAuthenticatedOrTokenHasResourceScope
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
            "200": inline_serializer(
                name="Teledeclarations",
                fields={
                    "teledeclarationIds": serializers.ListField(child=serializers.IntegerField()),
                    "errors": serializers.ListField(child=serializers.CharField()),
                },
            ),
        },
    )
    def post(self, request):
        data = request.data
        diagnostic_id = data.get("diagnostic_id")
        diagnostic_ids = data.get("diagnostic_ids")
        if not diagnostic_id and not diagnostic_ids:
            raise ValidationError("diagnosticId manquant")

        if not diagnostic_ids:
            td = TeledeclarationCreateView._teledeclare_diagnostic(diagnostic_id, request.user)

            data = FullDiagnosticSerializer(td.diagnostic).data
            return JsonResponse(camelize(data), status=status.HTTP_201_CREATED)
        else:
            td_ids = []
            errors = {}
            for d in diagnostic_ids:
                try:
                    td = TeledeclarationCreateView._teledeclare_diagnostic(d, request.user)
                    td_ids.append(td.id)
                except Exception as e:
                    message = getattr(e, "detail", "Autre erreur")
                    errors[d] = message[0] if type(message) == list else message
            return JsonResponse({"teledeclarationIds": td_ids, "errors": errors}, status=status.HTTP_200_OK)

    def _teledeclare_diagnostic(diagnostic_id, user):
        try:
            diagnostic = Diagnostic.objects.get(pk=diagnostic_id)
        except Diagnostic.DoesNotExist:
            raise PermissionDenied()  # in general we through 403s not 404s

        if user not in diagnostic.canteen.managers.all():
            raise PermissionDenied()

        try:
            Teledeclaration.validate_diagnostic(diagnostic)
        except DjangoValidationError as e:
            raise ValidationError(e.message) from e

        try:
            td = Teledeclaration.create_from_diagnostic(diagnostic, user)
            return td
        except DjangoValidationError as e:
            if hasattr(e, "message") and e.message == "Données d'approvisionnement manquantes":
                message = e.message
            else:
                message = "Il existe déjà une télédéclaration en cours pour cette année"
            raise ValidationError(message) from e


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
            teledeclaration_id = kwargs.get("pk")
            teledeclaration = Teledeclaration.objects.get(pk=teledeclaration_id)

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
        try:
            teledeclaration_id = kwargs.get("pk")

            if not teledeclaration_id:
                raise ValidationError("teledeclarationId manquant")

            teledeclaration = Teledeclaration.objects.get(pk=teledeclaration_id)
            if request.user not in teledeclaration.canteen.managers.all():
                raise PermissionDenied()

            if teledeclaration.status != Teledeclaration.TeledeclarationStatus.SUBMITTED:
                raise ValidationError("La télédéclaration n'est pas validée par l'utilisateur")

            response = HttpResponse(content_type="application/pdf")
            filename = TeledeclarationPdfView.get_filename(teledeclaration)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            template = get_template("teledeclaration_pdf.html")
            declared_data = teledeclaration.declared_data
            is_complete = (
                declared_data["teledeclaration"].get("diagnostic_type", None) == Diagnostic.DiagnosticType.COMPLETE
            )
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

            context = {
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
                },
            }
            html = template.render(context)
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=TeledeclarationPdfView.link_callback)

            if pisa_status.err:
                logger.error(
                    f"Error while generating PDF for teledeclaration {teledeclaration.id}:\n{pisa_status.err}"
                )
                return HttpResponse("An error ocurred", status=500)

            return response

        except Teledeclaration.DoesNotExist:
            raise ValidationError("La télédéclaration specifiée n'existe pas")

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
