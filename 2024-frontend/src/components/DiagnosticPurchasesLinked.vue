<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import { formatNumber } from "@/utils.js"
import AppBlueCard from "@/components/AppBlueCard.vue"

/* Store */
const purchaseSummaryStore = useStorePurchaseSummary()
const { purchaseSummary } = storeToRefs(purchaseSummaryStore)

/* Content */
const lastYear = new Date().getFullYear() - 1
const hasPurchase = computed(() => purchaseSummaryStore.hasPurchaseTotal(lastYear))
const purchaseAmount = computed(() => `${formatNumber(purchaseSummary.value[lastYear]?.valeurTotale)} €`)
</script>

<template>
  <AppBlueCard
    v-if="hasPurchase"
    title="Souhaitez-vous pré-remplir votre déclaration à partir de votre suivi d’achats ?"
    :alert="{
      description: 'Optionnel : cette étape n’est pas obligatoire pour déclarer vos approvisionnements.',
    }"
    :button="{
      label: 'Mettre à jour mes achats',
      to: 'PurchasesHome',
    }"
  >
    <p>
      Vous avez <strong>{{ purchaseAmount }}</strong> d’achats détectés dans votre suivi des achats. <br />
      Si vous utilisez l’Outil de Suivi des Achats (Mes achats), pour pré-remplir votre télédéclaration, assurez-vous d’avoir complété l’ensemble de vos achats de l’année précédente.
    </p>
  </AppBlueCard>
</template>
