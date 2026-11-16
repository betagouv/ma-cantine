from drf_spectacular.utils import extend_schema, extend_schema_view

from api.serializers import (
    DiagnosticVoletApprovisionnementV2Serializer,
    DiagnosticVoletDiversificationV2Serializer,
    DiagnosticVoletGaspillageV2Serializer,
    DiagnosticVoletInformationV2Serializer,
    DiagnosticVoletPlastiqueV2Serializer,
    DiagnosticV2Serializer,
)
from api.views.diagnostic import DiagnosticListCreateView, DiagnosticRetrieveUpdateView
from data.validators.diagnostic_teledeclaration import validate_is_in_teledeclaration_or_correction_period

# same permissions (session or OAuth2 with the "canteen" scope) as the v1 views they inherit from


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
        description="Uniquement les champs propres au bilan : les volets se modifient via leurs propres endpoints.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet approvisionnement d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet approvisionnement d'un bilan.",
        description="À noter que ce volet ne peut plus être modifié une fois le bilan télédéclaré. Pour ce faire, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletApprovisionnementV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletApprovisionnementV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet gaspillage alimentaire d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet gaspillage alimentaire d'un bilan.",
        description="À noter qu'une fois un bilan télédéclaré, seuls les champs des volets additionnels (hors approvisionnement) restent modifiables, et uniquement pendant la campagne. Pour modifier les autres champs, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletGaspillageV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletGaspillageV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet diversification des menus d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet diversification des menus d'un bilan.",
        description="À noter qu'une fois un bilan télédéclaré, seuls les champs des volets additionnels (hors approvisionnement) restent modifiables, et uniquement pendant la campagne. Pour modifier les autres champs, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletDiversificationV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletDiversificationV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet substitution du plastique d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet substitution du plastique d'un bilan.",
        description="À noter qu'une fois un bilan télédéclaré, seuls les champs des volets additionnels (hors approvisionnement) restent modifiables, et uniquement pendant la campagne. Pour modifier les autres champs, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletPlastiqueV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletPlastiqueV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le volet information des convives d'un bilan.",
        description="",
        tags=["Bilans (v2)"],
    ),
    patch=extend_schema(
        summary="Modifier le volet information des convives d'un bilan.",
        description="À noter qu'une fois un bilan télédéclaré, seuls les champs des volets additionnels (hors approvisionnement) restent modifiables, et uniquement pendant la campagne. Pour modifier les autres champs, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans (v2)"],
    ),
)
class DiagnosticVoletInformationV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletInformationV2Serializer
