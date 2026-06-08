<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"
import urlService from "@/services/urls.js"
import purchasesService from "@/services/purchases.js"
import AppLoader from "@/components/AppLoader.vue"
import AppRessources from "@/components/AppRessources.vue"
import PurchaseForm from "@/components/PurchaseForm.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Router and store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()
const forceRerender = ref(0)
const purchaseDeleted = ref(false)

/* Canteen */
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)

/* Purchase */
const isLoading = ref(true)
const purchaseId = route.params.id
const purchaseData = ref({})

const loadPurchase = async () => {
  isLoading.value = true
  const response = await purchasesService.fetchPurchase(purchaseId)
  if (!response?.id || response.canteen !== Number(canteenId)) {
    purchaseData.value = {}
  } else {
    purchaseData.value = response
  }
  isLoading.value = false
}

onMounted(loadPurchase)

/* Save */
const savePurchase = async (props) => {
  const { form } = props
  const response = await purchasesService.updatePurchase(form, purchaseId)

  if (!response?.id) {
    store.notifyServerError(response)
    return
  }

  purchaseData.value = response
  forceRerender.value++

  store.notify({
    title: "Achat mis à jour",
    message: `L'achat « ${form.description} » a bien été mis à jour pour la cantine « ${canteenName} ».`,
    status: "success",
  })

  // Pas de redirection car on arrive sur une page vue2 et on va perdre la notification
  window.scrollTo(0, 0)
}

/* Delete */
const deletePurchase = async () => {
  if (!purchaseId) return
  purchasesService.deletePurchase(purchaseId)
    .then(() => {
      purchaseDeleted.value = true
      purchaseData.value = {}
      forceRerender.value++
    })
    .catch(error => {
      store.notifyServerError(error)
    })
}

}

/* Redirect */
const goToPurchasesList = () => {
  router.push({ name: "PurchasesHome" })
}
</script>

<template>
  <DsfrAlert v-if="purchaseDeleted" class="fr-mt-4w" title="Achat supprimé" type="success">
    <p>
      L'achat a bien été supprimé pour la cantine « {{ canteenName }} ».
      <AppLinkRouter :to="{ name: 'PurchasesHome' }" title="Retourner à la liste des achats" />.
    </p>
  </DsfrAlert>
  <template v-else>
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
        :key="forceRerender"
        :purchase-data="purchaseData"
        :showCancelButton="true"
        :showDeleteButton="true"
        @sendForm="(payload) => savePurchase(payload)"
        @cancel="goToPurchasesList"
        @delete="deletePurchase"
      />
      <p v-else class="fr-mb-0" >
        Aucun achat trouvé avec le numéro d'identification « {{ purchaseId }} » pour la cantine « {{ canteenName }} ».
      </p>
    </section>

  </template>
</template>
