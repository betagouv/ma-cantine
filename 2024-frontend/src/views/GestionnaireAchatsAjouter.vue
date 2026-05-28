<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import urlService from "@/services/urls.js"
import purchasesService from "@/services/purchases.js"
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
  <h1>{{ route.meta.title }}</h1>
  <PurchaseForm
    :showCreateButton="true"
    :key="forceRerender"
    @sendForm="(payload) => savePurchase(payload)"
  />
</template>
