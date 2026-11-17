<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { formatNumber } from "@/utils"
import tunnelTeledeclarationService from "@/services/tunnelTeledeclaration"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationCalloutField from "@/components/TunnelTeledeclarationCalloutField.vue"
import CanteensTableCouvertsGroupe from "@/components/CanteensTableCouvertsGroupe.vue"

const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)
const route = useRoute()
const sumErrorMessage = computed(() => tunnelTeledeclarationService.getFieldError("nombreRepasAn", teledeclarationStore.getDisplayedErrors(route.meta)))
const nombreRepasAnSentence = computed(() => {
  const count = diagnostic.value?.nombreRepasAn
  if (count == null) return null
  const isPlural = count > 1
  return {
    count: `${formatNumber(count)} ${isPlural ? "couverts" : "couvert"}`,
    text: `${isPlural ? "ont été renseignés" : "a été renseigné"} automatiquement l’API ou via un import. Ce nombre doit être égal à la somme des couverts annuels de chacune des cantines de votre groupe. Si ce n’est pas le cas, veuillez modifier la donnée sur le fichier source.`,
  }
})
</script>

<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Vérifier le nombre de couverts annuels de mon groupe</h2>
      <p>Vous pouvez vérifier ici le total de couverts annuels de votre groupe. Le total des couverts annuels de votre groupe doit correspondre à la somme des couverts annuels de chacune des cantines du groupe. Si ce n’est pas le cas, vous pouvez ajuster les couverts annuels pour chaque cantine dans le tableau ci-dessous.</p>
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
    <h3 class="fr-h5">Vérifier la répartition des couverts annuels des cantines de votre groupe</h3>
    <p>Dans le tableau ci-dessous, vous trouverez la liste des cantines de votre groupe et leur nombre de couverts annuels. Prenez le temps de vérifier que la répartition est bonne afin d’assurer une donnée de qualité.</p>
    <DsfrAlert v-if="nombreRepasAnSentence" type="info" class="fr-mb-3w">
      <p>
        <span class="fr-text--bold">{{ nombreRepasAnSentence.count }}</span> {{ nombreRepasAnSentence.text }}
      </p>
    </DsfrAlert>
    <TunnelTeledeclarationCalloutField
      text="Total des couverts annuels répartis entre vos cantines"
      mention="À partir des données couverts de chaque restaurant"
      :value="diagnostic?.satellitesNombreRepasAnSum"
      :error-message="sumErrorMessage"
    />
    <CanteensTableCouvertsGroupe />
  </div>
</template>
