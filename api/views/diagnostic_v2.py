from drf_spectacular.utils import extend_schema, extend_schema_view

from api.serializers import (
    DiagnosticVoletApprovisionnementV2Serializer,
    DiagnosticVoletDiversificationV2Serializer,
    DiagnosticVoletGaspillageV2Serializer,
    DiagnosticVoletInformationV2Serializer,
    DiagnosticVoletPlastiqueV2Serializer,
    DiagnosticV2Serializer,
)
from django.core.exceptions import ValidationError

from api.views.diagnostic import DiagnosticListCreateView, DiagnosticRetrieveUpdateView
from data.models.diagnostic_teledeclaration_dates import get_current_campaign_year
from data.validators.diagnostic_teledeclaration import validate_is_in_teledeclaration_or_correction_period

# same permissions (session or OAuth2 with the "canteen" scope) as the v1 views they inherit from

UPDATE_DESCRIPTION_CAMPAIGN = "Uniquement pendant la campagne (télédéclaration ou correction), et pour le bilan de l'année de la campagne en cours."
VOLET_ADDITIONNEL_UPDATE_DESCRIPTION = f"{UPDATE_DESCRIPTION_CAMPAIGN} À noter qu'une fois un bilan télédéclaré, seuls les champs des volets additionnels (hors approvisionnement) restent modifiables. Pour modifier les autres champs, il faut d'abord annuler la télédéclaration."


class DiagnosticV2RetrieveUpdateCampaignView(DiagnosticRetrieveUpdateView):
    """
    Like the imports & the creation: a diagnostic can only be updated during the campaign (teledeclaration or correction),
    and only the diagnostic of the current campaign year
    """

    def perform_update(self, serializer):
        validate_is_in_teledeclaration_or_correction_period("update")
        campaign_year = get_current_campaign_year()
        if serializer.instance.year != campaign_year:
            raise ValidationError(
                f"Ce n'est pas possible de modifier un bilan d'une autre année que celle de la campagne en cours ({campaign_year})"
            )
        super().perform_update(serializer)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les bilans d'une cantine.",
        description="Chaque bilan contient les champs de tous ses volets (selon son année).",
        tags=["Bilans (v2)"],
    ),
    post=extend_schema(
        summary="Créer un nouveau bilan.",
        description="Un bilan doit être rattaché à une cantine. Les volets se remplissent ensuite via leurs propres endpoints. L'année n'est pas demandée : le bilan est celui de l'année de la campagne en cours (ex : bilan 2026 pendant la campagne de début 2027). La création n'est possible que pendant la campagne (télédéclaration ou correction).",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticV2ListCreateView(DiagnosticListCreateView):
    serializer_class = DiagnosticV2Serializer

    def perform_create(self, serializer):
        # like the imports: only during the campaign (the year is the current campaign year, see the serializer)
        validate_is_in_teledeclaration_or_correction_period("create")
        super().perform_create(serializer)


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer un bilan existant.",
        description="Le bilan contient les champs de tous ses volets (selon son année).",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier un bilan existant.",
        description=f"Uniquement les champs propres au bilan : les volets se modifient via leurs propres endpoints. {UPDATE_DESCRIPTION_CAMPAIGN}",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticV2RetrieveUpdateView(DiagnosticV2RetrieveUpdateCampaignView):
    serializer_class = DiagnosticV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet approvisionnement d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet approvisionnement d'un bilan.",
        description=f"{UPDATE_DESCRIPTION_CAMPAIGN} À noter que ce volet ne peut plus être modifié une fois le bilan télédéclaré. Pour ce faire, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletApprovisionnementV2RetrieveUpdateView(DiagnosticV2RetrieveUpdateCampaignView):
    serializer_class = DiagnosticVoletApprovisionnementV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet gaspillage alimentaire d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet gaspillage alimentaire d'un bilan.",
        description=VOLET_ADDITIONNEL_UPDATE_DESCRIPTION,
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletGaspillageV2RetrieveUpdateView(DiagnosticV2RetrieveUpdateCampaignView):
    serializer_class = DiagnosticVoletGaspillageV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet diversification des menus d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet diversification des menus d'un bilan.",
        description=VOLET_ADDITIONNEL_UPDATE_DESCRIPTION,
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletDiversificationV2RetrieveUpdateView(DiagnosticV2RetrieveUpdateCampaignView):
    serializer_class = DiagnosticVoletDiversificationV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet substitution du plastique d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet substitution du plastique d'un bilan.",
        description=VOLET_ADDITIONNEL_UPDATE_DESCRIPTION,
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletPlastiqueV2RetrieveUpdateView(DiagnosticV2RetrieveUpdateCampaignView):
    serializer_class = DiagnosticVoletPlastiqueV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet information des convives d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet information des convives d'un bilan.",
        description=VOLET_ADDITIONNEL_UPDATE_DESCRIPTION,
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletInformationV2RetrieveUpdateView(DiagnosticV2RetrieveUpdateCampaignView):
    serializer_class = DiagnosticVoletInformationV2Serializer
