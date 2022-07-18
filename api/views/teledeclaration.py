import logging
import os
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError as DjangoValidationError
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings
from django.utils.text import slugify
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from xhtml2pdf import pisa
from data.models import Diagnostic, Teledeclaration
from api.serializers import FullDiagnosticSerializer
from api.permissions import IsAuthenticated
from .utils import camelize

logger = logging.getLogger(__name__)


class TeledeclarationCreateView(APIView):
    """
    This view allows creating a teledeclaration from an
    existing diagnostic.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            diagnostic_id = data.get("diagnostic_id")
            if not diagnostic_id:
                raise ValidationError("diagnosticId manquant")

            diagnostic = Diagnostic.objects.get(pk=diagnostic_id)
            if request.user not in diagnostic.canteen.managers.all():
                raise PermissionDenied()

            TeledeclarationCreateView.validateDiagnostic(diagnostic)
            Teledeclaration.createFromDiagnostic(diagnostic, request.user)

            data = FullDiagnosticSerializer(diagnostic).data
            return JsonResponse(camelize(data), status=status.HTTP_201_CREATED)

        except Diagnostic.DoesNotExist:
            raise ValidationError("Le diagnostic specifié n'existe pas")

        except DjangoValidationError as e:
            message = "Il existe déjà une télédéclaration en cours pour cette année"
            raise ValidationError(message) from e

    @staticmethod
    def validateDiagnostic(diagnostic):
        total_ht = diagnostic.value_total_ht
        breakdown = [
            diagnostic.value_sustainable_ht,
            diagnostic.value_bio_ht,
            diagnostic.value_externality_performance_ht,
            diagnostic.value_egalim_others_ht,
            diagnostic.value_meat_poultry_ht,
            diagnostic.value_meat_poultry_egalim_ht,
            diagnostic.value_meat_poultry_france_ht,
            diagnostic.value_fish_ht,
            diagnostic.value_fish_egalim_ht,
        ]
        if not total_ht or None in breakdown:
            raise ValidationError("Données d'approvisionnement manquantes")


class TeledeclarationCancelView(APIView):
    """
    This view cancels a submitted teledeclaration
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            teledeclaration_id = data.get("teledeclaration_id")
            if not teledeclaration_id:
                raise ValidationError("teledeclarationId manquant")

            teledeclaration = Teledeclaration.objects.get(pk=teledeclaration_id)

            if request.user not in teledeclaration.canteen.managers.all():
                raise PermissionDenied()

            teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
            teledeclaration.save()

            data = FullDiagnosticSerializer(teledeclaration.diagnostic).data
            return JsonResponse(camelize(data), status=status.HTTP_200_OK)

        except Teledeclaration.DoesNotExist:
            raise ValidationError("La télédéclaration specifiée n'existe pas")


class TeledeclarationPdfView(APIView):
    """
    This view returns a PDF for proof of teledeclaration
    """

    permission_classes = [IsAuthenticated]

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
            context = {
                **declared_data["teledeclaration"],
                **{
                    "year": teledeclaration.year,
                    "canteen_name": declared_data["canteen"]["name"],
                    "siret": declared_data["canteen"]["siret"],
                    "date": teledeclaration.creation_date,
                    "applicant": declared_data["applicant"]["name"],
                },
            }
            html = template.render(context)
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=TeledeclarationPdfView.link_callback)

            if pisa_status.err:
                logger.error(f"Error while generating PDF for teledeclaration {teledeclaration.id}")
                logger.error(pisa_status.err)
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
