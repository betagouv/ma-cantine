<script setup>
import { ref } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import urlService from "@/services/urls.js"
import purchasesService from "@/services/purchases.js"
import AppLoader from "@/components/AppLoader.vue"
import AppRessources from "@/components/AppRessources.vue"
import PurchaseForm from "@/components/PurchaseForm.vue"

/* Router and store */
const route = useRoute()

/* Canteen */
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)

/* Purchase */
const isLoading = ref(true)
const purchaseId = route.params.id

const purchaseData = computedAsync(async () => {
  const response = await purchasesService.fetchPurchase(purchaseId)
  isLoading.value = false
  return !response?.id ? {} : response
}, {})

/* Save */
const savePurchase = async (props) => {
  console.log(props)
}
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-6 fr-mb-4w fr-mb-md-0">
      <h1>{{ route.meta.title }} pour la cantine «&nbsp;{{ canteenName }}&nbsp;»</h1>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a :href="documentation.ajouterAchat" target="_blank">
          Tutoriel pour ajouter un achat manuellement
        </a>
      </li>
      <li>
        <a :href="documentation.critèresQualiteDurabiliteProduits" target="_blank">
          Comprendre les critères de qualité et durabilité des produits
        </a>
      </li>
    </AppRessources>
  </section>
  <section
    class="fr-background-alt--blue-france fr-p-3w fr-mt-4w fr-grid-row fr-grid-row--center"
  >
    <AppLoader v-if="isLoading" />
    <PurchaseForm
      v-else-if="purchaseData.id"
      :purchase-data="purchaseData"
      :showCancelButton="true"
      @sendForm="(payload) => savePurchase(payload)"
      @cancel="goToPurchasesList"
    />
    <p v-else class="fr-mb-0" >
      Aucun achat trouvé avec le numéro d'identification « {{ purchaseId }} » pour la cantine « {{ canteenName }} ».
    </p>
  </section>
</template>
