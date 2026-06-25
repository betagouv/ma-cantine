<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"
import urlService from "@/services/urls.js"
import purchasesService from "@/services/purchases.js"
import AppRessources from "@/components/AppRessources.vue"
import PurchaseForm from "@/components/PurchaseForm.vue"

/* Router and store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()

/* Canteen */
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)

/* Save purchase */
const forceRerender = ref(0)

const savePurchase = async (props) => {
  const { form, action } = props
  const payload = { ...form, canteen: canteenId }
  const response = await purchasesService.createPurchase(payload)

  if (!response?.id) {
    store.notifyServerError(response)
    return
  }

  store.notify({
    title: "Achat enregistré",
    message: `L'achat « ${form.description} » a bien été enregistré pour la cantine « ${canteenName} ».`,
    status: "success",
  })

  if (action === "stay-on-creation-page") resetForm()
  if (action === "go-to-purchases-list") goToPurchasesList()
}

/* After purchase is saved */
const goToPurchasesList = () => {
  router.push({ name: "PurchasesHome" })
}

const resetForm = () => {
  window.scrollTo(0, 0)
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
  <PurchaseForm
    :showCreateButton="true"
    :key="forceRerender"
    @sendForm="(payload) => savePurchase(payload)"
  />
</template>
