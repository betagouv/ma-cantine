<template>
  <DsfrCallout noIcon class="mt-2">
    <h2 class="fr-text font-weight-bold mb-2 mt-2">
      <span class="text-uppercase">Droit à l'erreur :</span>
      du 16 au 30 avril 2025
    </h2>
    <p class="mb-2">
      Valable uniquement pour les établissements qui ont validé leur télédéclaration.
    </p>
    <ul>
      <li>
        Correction des volets EGalim
      </li>
      <li>
        Pour les cuisines centrales, ajout des cuisines satellites manquants
      </li>
      <li>
        Correction des caractéristiques de la cantine (SIRET, type d’établissement, nombre de couverts..)
      </li>
    </ul>
  </DsfrCallout>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"

export default {
  name: "InformationBanner",
  components: {
    DsfrCallout,
  },
}
</script>
