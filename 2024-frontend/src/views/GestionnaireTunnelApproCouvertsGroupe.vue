<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { formatNumber } from "@/utils"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationCallout from "@/components/TunnelTeledeclarationCallout.vue"
import TunnelTeledeclarationLockedInput from "@/components/TunnelTeledeclarationLockedInput.vue"
import CanteensTableCouvertsGroupe from "@/components/CanteensTableCouvertsGroupe.vue"

const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)
const nombreRepasAnSentence = computed(() => {
  const count = diagnostic.value?.nombreRepasAn
  if (count == null) return null
  const isPlural = count > 1
  return {
    count: `${formatNumber(count)} ${isPlural ? "couverts" : "couvert"}`,
    text: `${isPlural ? "ont été renseignés" : "a été renseigné"} via API ou import. Votre répartition doit être identique, ou modifier votre import.`,
  }
})
</script>

<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Estimer le nombre de couverts de mon groupe</h2>
      <p>Vous devez détailler la répartition entre toutes les cantines du groupe et l’ajuster à l’aide du tableau ci-dessous.</p>
      <p>Par défaut, le nombre de couverts de chaque cantine est prérempli à partir du nombre de couverts annuels renseigné dans leurs informations.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Ajuster mes établissements">
        <ul class="ma-cantine--unstyled-list">
          <li><a target="_blank" :href="documentation.calculerNombreCouverts">Utiliser l’outil de calcul</a></li>
          <li><a target="_blank" :href="documentation.couvertsGroupeCantineManquante">Il me manque une cantine dans ma répartition de couvert, que faire ?</a></li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <div>
    <h3 class="fr-h5">Renseigner la répartition de mes couverts annuels entre mes cantines :</h3>
    <p>Pour avoir une donnée de qualité vous devez ajuster la répartition du nombre de couvert pour chaque cantine dans le tableau ci-dessous.<template v-if="nombreRepasAnSentence"> L'estimation et la répartition des couverts entre vos établissement doit correspondre.</template></p>
    <DsfrAlert v-if="nombreRepasAnSentence" type="info" class="fr-mb-3w">
      <p>
        <span class="fr-text--bold">{{ nombreRepasAnSentence.count }}</span> {{ nombreRepasAnSentence.text }}
      </p>
    </DsfrAlert>
    <TunnelTeledeclarationCallout
      :col-sizes="{ left: 10, right: 2 }"
      text="Total des couverts annuels répartis entre vos cantines"
      mention="À partir des données couverts de chaque restaurant"
    >
      <TunnelTeledeclarationLockedInput :value="diagnostic?.satellitesNombreRepasAnSum" label="Total des couverts annuels répartis entre vos cantines" />
    </TunnelTeledeclarationCallout>
    <CanteensTableCouvertsGroupe />
  </div>
</template>
