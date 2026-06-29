<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"
import urlService from "@/services/urls.js"
import purchasesService from "@/services/purchases.js"
import AppRessources from "@/components/AppRessources.vue"
import PurchaseForm from "@/components/PurchaseForm.vue"
import PurchaseFormSuccessModal from "@/components/PurchaseFormSuccessModal.vue"

/* Props */
const route = useRoute()
const store = useRootStore()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const forceRerender = ref(0)
const purchaseCreatedId = ref(null)

/* Save purchase */
const savePurchase = async (form) => {
  const payload = { ...form, canteen: canteenId }
  const response = await purchasesService.createPurchase(payload)
  if (!response?.id) store.notifyServerError(response)
  else purchaseCreatedId.value = response.id
}

/* Reset form */
const resetForm = () => {
  window.scrollTo(0, 0)
  purchaseCreatedId.value = null
  forceRerender.value++
}
</script>

<template>
  <section class="fr-grid-row fr-grid-row--middle fr-mb-4w">
    <div class="fr-col-12 fr-col-md-6 fr-mb-4w fr-mb-md-0">
      <h1>{{ route.meta.title }}</h1>
      <p>
        Pour la cantine «&nbsp;{{ canteenName }}&nbsp;»
      </p>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a :href="documentation.suiviAchatsEgalim" target="_blank">
          En savoir plus sur l'outil de suivi des achats EGalim
        </a>
      </li>
      <li>
        <a :href="documentation.critèresQualiteDurabiliteProduits" target="_blank">
          Comprendre les critères de qualité et durabilité des produits
        </a>
      </li>
    </AppRessources>
  </section>
  <PurchaseForm
    :key="forceRerender"
    @sendForm="(payload) => savePurchase(payload)"
  />
  <PurchaseFormSuccessModal
    v-if="purchaseCreatedId"
    :purchaseId="purchaseCreatedId"
    @close="resetForm"
  />
</template>
