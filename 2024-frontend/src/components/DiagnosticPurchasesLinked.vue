<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import { formatNumber } from "@/utils.js"
import { useRouter } from "vue-router"

/* Store */
const router = useRouter()
const purchaseSummaryStore = useStorePurchaseSummary()
const { purchaseSummary, hasPurchaseTotal } = storeToRefs(purchaseSummaryStore)
const purchaseAmount = computed(() => `${formatNumber(purchaseSummary.value?.valeurTotale)} €`)
const iconLink = "/static/images/picto-dsfr/teledeclaration-saisie-automatique.svg"

/* Actions */
const goToPurchases = () => {
  router.push({ name: 'PurchasesHome' })
}
</script>

<template>
  <div class="diagnostic-purchases-linked fr-background-alt--blue-france fr-p-4w">
    <div class="diagnostic-purchases-linked__top">
      <img :src="iconLink" alt="Logo outil Mes achats" class="diagnostic-purchases-linked__icon fr-mb-2w" />
      <p class="diagnostic-purchases-linked__title fr-text--bold">Souhaitez-vous modifier votre déclaration en pré-remplissant une nouvelle déclaration à partir de votre suivi d’achats (outil “Mes achats”) ?</p>
      <DsfrButton label="En savoir plus" icon="ri-information-line" secondary class="diagnostic-purchases-linked__button" size="sm" />
    </div>
    <p v-if="hasPurchaseTotal" class="fr-mb-1w">
      Vous avez <span class="fr-text--bold">{{ purchaseAmount }}</span> d’achats détectés dans votre suivi des achats.
    </p>
    <p v-else class="fr-mb-1w">
      Vous n’avez pas d’achats détectés dans votre suivi des achats.
    </p>
    <p>
      Si vous utilisez l’Outil de suivi des achats, pour pré-remplir votre télédéclaration, assurez-vous d’avoir complété l’ensemble de vos achats de l’année précédente.
    </p>
    <DsfrButton label="Consulter Mes Achats" @click="goToPurchases" secondary />
  </div>
</template>
<style scoped lang="scss">
.diagnostic-purchases-linked {
  &__top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 2rem;
  }

  &__title {
    flex-shrink: 1;
  }

  &__button {
    flex-shrink: 0;
  }

  &__icon {
    width: 4rem;
    height: 4rem;
  }
}
</style>
