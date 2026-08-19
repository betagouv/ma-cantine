<script setup>
import { useStoreCanteen } from "@/stores/canteen.js"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import CanteenDisplayInformations from "@/components/CanteenDisplayInformations.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const route = useRoute()
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
</script>
<template>
  <p class="fr-mb-4w">
    <span v-if="canteenInformations.isGroupe">C’est le moment de vérifier les informations de votre établissement et en tant qu’entité de gestion d’un groupe.</span>
    <span v-else>C’est le moment de vérifier les informations de votre cantine (nom, gestionnaire, effectifs, mode de gestion, etc.).</span>
    Si vous remarquez des erreurs, corriger-les avant de passer à l'étape suivante <AppLinkRouter title="en cliquant ici" :to="{name: canteenInformations.isGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier', query: { redirection: route.fullPath }}" />
  </p>
  <CanteenDisplayInformations :canteen-information="canteenInformations" :canteen-is-groupe="canteenInformations.isGroupe" />
</template>
