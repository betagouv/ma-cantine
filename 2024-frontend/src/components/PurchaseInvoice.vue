<script setup>
import { toBase64 } from "@/utils.js"
import { ref, onMounted} from "vue"
import { useRootStore } from "@/stores/root"
import purchasesService from "@/services/purchases.js"
import AppLoader from "@/components/AppLoader.vue"

/* Props */
const store = useRootStore()
const props = defineProps(["purchaseId", "canteenId"])
const isLoading = ref(true)
const invoiceUrl = ref(null)
const isUploadingInvoice = ref(false)

/* Get from purchase */
const loadInvoice = async () => {
  isLoading.value = true
  purchasesService.fetchInvoice(props.canteenId, props.purchaseId)
    .then(response => invoiceUrl.value = response.facture)
    .catch(() => invoiceUrl.value = null)
    .finally(() => isLoading.value = false)
}
onMounted(loadInvoice)

/* Max size */
const invoiceMaxSize = 10 * 1024 * 1024 // 10 Mo
const invoiceFile = ref(null)
const invoiceFileInputValue = ref("")
const invoiceFileError = ref("")

const onInvoiceFileChange = (files) => {
  invoiceFileError.value = ""
  const file = files?.[0]
  if (!file) {
    invoiceFile.value = null
    return
  }
  if (file.size > invoiceMaxSize) {
    invoiceFileError.value = "Le fichier dépasse la taille maximale de 10 Mo."
    invoiceFile.value = null
    return
  }
  uploadInvoice(file)
}

/* Upload */
const uploadInvoice = async (file) => {
  isUploadingInvoice.value = true
  const invoiceBase64 = await toBase64(file)
  const payload = {
    canteenId: props.canteenId,
    purchaseId: props.purchaseId,
    body: {
      facture: invoiceBase64,
    }
  }
  purchasesService.uploadInvoice(payload).then(response => {
    invoiceUrl.value = response.facture
    invoiceFileInputValue.value = null
    store.notify({
      title: "Facture enregistrée",
      message: "La facture de l'achat a bien été enregistrée.",
      status: "success",
    })
  }).catch(error => store.notifyServerError(error))
  .finally(() => isUploadingInvoice.value = false)
}

/* Open invoice file */
const openInvoice = () => {
  window.open(invoiceUrl.value, "_blank")
}

/* Delete */
const deleteInvoice = async () => {
  isUploadingInvoice.value = true
  purchasesService.deleteInvoice(props.canteenId, props.purchaseId)
    .then(() => {
      invoiceUrl.value = null
      store.notify({
        title: "Facture supprimée",
        message: "La facture de l'achat a bien été supprimée.",
        status: "success",
      })
    })
    .catch(error => store.notifyServerError(error))
    .finally(() => isUploadingInvoice.value = false)
}
</script>
<template>
  <div class="fr-card fr-p-3w fr-background-alt--grey">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-8">
        <p class="fr-h6 fr-mb-1w"><span class="fr-icon-file-line"></span> Facture</p>
        <p class="fr-text--sm fr-mb-0">Ce champ est facultatif. Il n'est pas nécessaire d'importer ses factures pdf si vous disposez déjà d'un espace de stockage fiable et sécurisé (sur votre ordinateur ou autre logiciel par exemple).</p>
        <div v-if="invoiceUrl" class="purchase-invoice__actions fr-mt-3w">
          <DsfrButton
            :disabled="isUploadingInvoice"
            label="Voir la facture"
            secondary
            icon="fr-icon-eye-line"
            @click="openInvoice"
          />
          <DsfrButton
            :disabled="isUploadingInvoice"
            label="Supprimer le fichier"
            tertiary
            icon="fr-icon-delete-line"
            @click="deleteInvoice"
          />
        </div>
      </div>
      <div class="purchase-invoice__file-upload fr-col-12 fr-col-md-4 fr-pb-3w">
        <DsfrFileUpload
          v-model="invoiceFileInputValue"
          :label="invoiceUrl ? 'Télécharger une nouvelle facture' : 'Télécharger une facture'"
          hint="PDF ou image (JPEG, PNG) — 10 Mo maximum"
          accept="image/jpeg,image/png,application/pdf"
          :error="invoiceFileError"
          @change="onInvoiceFileChange"
        />
        <AppLoader v-if="isUploadingInvoice" />
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.purchase-invoice {
  &__actions {
    display: flex;
    gap: 1rem;
  }
}
</style>
