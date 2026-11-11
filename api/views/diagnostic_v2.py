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

# same permissions (session or OAuth2 with the "canteen" scope) as the v1 views they inherit from

TAGS = ["Bilans (v2)"]
TELEDECLARED_PATCH_DESCRIPTION = "À noter qu'une fois un bilan télédéclaré, seuls les champs des volets additionnels (hors approvisionnement) restent modifiables, et uniquement pendant la campagne. Pour modifier les autres champs, il faut d'abord annuler la télédéclaration."


def volet_schema_view(volet_name, patch_description=TELEDECLARED_PATCH_DESCRIPTION):
    return extend_schema_view(
        get=extend_schema(summary=f"Récupérer le volet {volet_name} d'un bilan.", description="", tags=TAGS),
        patch=extend_schema(
            summary=f"Modifier le volet {volet_name} d'un bilan.", description=patch_description, tags=TAGS
        ),
    )


@extend_schema_view(
    get=extend_schema(
        summary="Lister les bilans d'une cantine.",
        description="Chaque bilan contient les champs de tous ses volets (selon son année).",
        tags=TAGS,
    ),
    post=extend_schema(
        summary="Créer un nouveau bilan.",
        description="Un bilan doit être rattaché à une cantine. Les volets se remplissent ensuite via leurs propres endpoints.",
        tags=TAGS,
    ),
)
class DiagnosticV2ListCreateView(DiagnosticListCreateView):
    serializer_class = DiagnosticV2Serializer


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer un bilan existant.",
        description="Le bilan contient les champs de tous ses volets (selon son année).",
        tags=TAGS,
    ),
    patch=extend_schema(
        summary="Modifier un bilan existant.",
        description="Uniquement les champs propres au bilan : les volets se modifient via leurs propres endpoints.",
        tags=TAGS,
    ),
)
class DiagnosticV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticV2Serializer


@volet_schema_view(
    "approvisionnement",
    patch_description="À noter que ce volet ne peut plus être modifié une fois le bilan télédéclaré. Pour ce faire, il faut d'abord annuler la télédéclaration.",
)
class DiagnosticVoletApprovisionnementV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletApprovisionnementV2Serializer


@volet_schema_view("gaspillage alimentaire")
class DiagnosticVoletGaspillageV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletGaspillageV2Serializer


@volet_schema_view("diversification des menus")
class DiagnosticVoletDiversificationV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletDiversificationV2Serializer


@volet_schema_view("substitution du plastique")
class DiagnosticVoletPlastiqueV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletPlastiqueV2Serializer


@volet_schema_view("information des convives")
class DiagnosticVoletInformationV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    serializer_class = DiagnosticVoletInformationV2Serializer
