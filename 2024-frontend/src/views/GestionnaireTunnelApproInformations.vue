<script setup>
import { computed } from "vue"
import { useStoreCanteen } from "@/stores/canteen.js"
import { storeToRefs } from "pinia"
import { useRouter, useRoute } from "vue-router"
import CanteenDisplayInformations from "@/components/CanteenDisplayInformations.vue"

const router = useRouter()
const route = useRoute()
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)

/* Button */
const label = computed(() => canteenInformations.isGroupe ? 'Modifier les informations de mon groupe' : 'Modifier mes informations')
const gotTo = () => {
  router.push({name: canteenInformations.isGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier', query: { redirection: route.fullPath }})
}
</script>
<template>
  <div class="ma-cantine--flex-between ma-cantine--flex-gap-2 ma-cantine--flex-top fr-mb-4w">
    <p class="fr-mb-0">
      <span v-if="canteenInformations.isGroupe">C’est le moment de vérifier les informations de votre établissement et en tant qu’entité de gestion d’un groupe.</span>
      <span v-else>C’est le moment de vérifier les informations de votre cantine (nom, gestionnaire, effectifs, mode de gestion, etc.).</span>
      Si vous remarquez des erreurs, corriger-les avant de passer à l'étape suivante.
    </p>
    <DsfrButton
      class="ma-cantine--flex-shrink-0"
      :label="label"
      icon="fr-icon-edit-line"
      @click="gotTo"
    />
  </div>
  <CanteenDisplayInformations :canteen-information="canteenInformations" :canteen-is-groupe="canteenInformations.isGroupe" />
</template>
