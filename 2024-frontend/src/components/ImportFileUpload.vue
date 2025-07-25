<script setup>
import AppSeparator from "@/components/AppSeparator.vue"
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import { trackEvent } from "@/services/matomo.js"
import { importFile } from "@/services/imports.js"

/* Store and Router and Emit and Props */
const store = useRootStore()
const router = useRouter()
const emit = defineEmits(["success"])
const props = defineProps(["apiUrl", "eventMatomo"])

/* Data */
const pictoDocument = "/static/images/picto-dsfr/document-add.svg"

/* Upload */
const isProcessingFile = ref(false)
const upload = (file) => {
  if (isProcessingFile.value) return
  isProcessingFile.value = true
  initErrors()
  importFile({ file: file, apiUrl: props.apiUrl })
    .then((json) => {
      if (json.count >= 1) successUpload({ seconds: json.seconds, count: json.count })
      else if (json.duplicateFile) duplicatedUpload(json.duplicatePurchases)
      else if (json.errorCount > 0) errorUpload({ count: json.errorCount, errors: json.errors })
      else if (json.errors.length > 0) errorUpload({ count: json.errors.length, errors: json.errors })
      isProcessingFile.value = false
    })
    .catch((e) => {
      store.notifyServerError(e)
      isProcessingFile.value = false
    })
}

const successUpload = (params) => {
  const { seconds, count } = params
  const message = `Fichier traité en ${Math.round(seconds)} secondes`
  store.notify({ message })
  emit("success", count)
  trackEvent({ category: "inquiry", action: "send", value: props.eventMatomo })
}

const duplicatedUpload = (purchases) => {
  const countPurchases = purchases.length
  const message =
    countPurchases > 1
      ? `Ce fichier a déjà été utilisé pour importer ${countPurchases} achats :`
      : "Ce fichier a déjà été utilisé pour importer 1 achat :"
  hasErrors.list = [
    {
      message,
      purchases,
    },
  ]
  showErrors(1)
}

const groupErrorsByColumn = (errors) => {
  const groupedErrors = []
  errors.forEach((error) => {
    const errorMessage = error.title ? error.title : error.message // Validata: we display the 'title' instead of the 'message'
    let index = groupedErrors.findIndex(
      (groupedError) => groupedError.field === error.field && groupedError.message === errorMessage
    )
    if (index === -1) {
      groupedErrors.push({
        field: error.field,
        message: errorMessage,
        rowList: [],
        showLink: error.has_doc,
      })
      index = groupedErrors.length - 1
    }
    if (error.row > 0) {
      groupedErrors[index].rowList.push(error.row)
    }
  })
  // TODO: order by column from left to right
  return groupedErrors
}

const errorUpload = (props) => {
  const { count, errors } = props
  showErrors(count)
  hasErrors.list = groupErrorsByColumn(errors)
}

const hasErrors = reactive({})
const initErrors = () => {
  hasErrors.status = false
  hasErrors.badge = ""
  hasErrors.message = ""
  hasErrors.list = []
}
initErrors()
const showErrors = (count) => {
  hasErrors.status = true
  hasErrors.badge = count > 1 ? `${count} Erreurs détectées` : "1 Erreur détectée"
  hasErrors.message =
    count > 1
      ? "Veuillez les corriger avant d’importer à nouveau le fichier."
      : "Veuillez la corriger avant d’importer à nouveau le fichier."
  router.push("#file-upload")
}
</script>

<template>
  <section
    id="file-upload"
    class="fr-px-6w fr-px-xl-9w fr-py-6w fr-background-alt--blue-france fr-mt-4w fr-grid-row fr-grid-row--middle"
  >
    <div class="fr-hidden fr-unhidden-xl fr-col-3 fr-pr-6w fr-grid-row--center">
      <img :src="pictoDocument" alt="" />
    </div>
    <div class="import-file-upload fr-col-12 fr-col-xl-9 fr-py-3w fr-px-4w fr-card">
      <DsfrFileUpload
        label="Avant d’importer votre fichier en CSV, assurez-vous que vos données respectent le format ci-dessus"
        hint="Extension du fichier autorisé : CSV"
        accept=".csv,.tsv"
        @change="upload"
        :disabled="isProcessingFile"
      />
      <div v-if="hasErrors.status" class="fr-mt-2w">
        <div class="fr-grid-row fr-grid-row--middle">
          <DsfrBadge type="error" :label="hasErrors.badge" />
          <p class="fr-text-default--error fr-ml-1w fr-mb-0 fr-mt-1w fr-mt-md-0">
            {{ hasErrors.message }}
          </p>
        </div>
        <AppSeparator class="fr-my-3w" />
        <ul>
          <li v-for="(error, index) in hasErrors.list" :key="index" class="fr-text-default--error">
            <p class="fr-mb-1v">
              <span v-if="error.field" class="ma-cantine--bold">{{ error.field }} :</span>
              {{ error.message }}
            </p>
            <ul v-if="error.purchases" class="ma-cantine--unstyled-list fr-text-default--grey">
              <li v-for="(purchase, index) in error.purchases" :key="index">
                {{ purchase.description }} | {{ purchase.date }} | {{ purchase.priceHt }}€
              </li>
            </ul>
            <p v-if="error.rowList?.length" class="fr-text-default--grey fr-mb-0">
              {{ error.rowList.length }} ligne{{ error.rowList.length > 1 ? "s" : "" }} concernée{{
                error.rowList.length > 1 ? "s" : ""
              }}
              par cette erreur : {{ error.rowList.join(", ") }}
              <router-link
                v-if="error.showLink"
                class="fr-ml-1w"
                :to="{ hash: `#${error.field}`, params: { scrollTop: 75 } }"
              >
                Voir le format attendu
              </router-link>
            </p>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style lang="scss">
.import-file-upload {
  .fr-label {
    font-weight: 700;
    max-width: 75%;

    span {
      font-weight: initial;
    }
  }
}
</style>
