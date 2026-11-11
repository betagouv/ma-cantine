<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)

const hasDonsConvention = computed(() => diagnostic.value.donsConvention === true)
const updateDonsConvention = (value) => {
  if (value === true) return
  storeTeledeclaration.setValue("donsFrequence", null)
  storeTeledeclaration.setValue("donsQuantite", null)
  storeTeledeclaration.setValue("donsTypeDenrees", null)
}
</script>

<template>
  <h2>Lutte contre le gaspillage alimentaire et dons alimentaires</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-1w">
        La lutte contre le gaspillage alimentaire est un levier essentiel pour l’atteinte des objectifs de la loi EGalim.
        Les obligations concernent :
      </p>
      <ul class="fr-mb-0">
        <li>
          <span class="fr-text--bold">réaliser un diagnostic et un plan d’actions :</span> pour tous les établissements
        </li>
        <li>
          <span class="fr-text--bold">proposer une convention de don à une association d’aide alimentaire habilitée :</span> uniquement aux opérateurs servant plus de 3000 repas
          par jour (loi EGalim). Vous pouvez en proposer une même si vous n’êtes pas soumis à l’obligation.
        </li>
      </ul>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur vos obligations">
        <a :href="documentation.lutteGaspillageDonsAlimentaires" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Diagnostic et plan d’actions" />
    <TunnelTeledeclarationField name="diagnosticGaspillageRealise" />
    <TunnelTeledeclarationField name="planGaspillageEnPlace" />
    <TunnelTeledeclarationField name="actionsGaspillageRealisees" />
    <TunnelTeledeclarationField name="actionsGaspillageAutre" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Dons alimentaires" />
    <TunnelTeledeclarationField name="donsConvention" @change="updateDonsConvention" />
    <div v-if="hasDonsConvention" class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="donsFrequence" />
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="donsQuantite" />
      </div>
      <div class="fr-col-12">
        <TunnelTeledeclarationField name="donsTypeDenrees" />
      </div>
    </div>
  </div>
</template>
