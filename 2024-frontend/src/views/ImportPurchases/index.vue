<script setup>
import { reactive, ref } from "vue"
import { useRootStore } from "@/stores/root"
import { importPurchases } from "@/services/imports.js"
import { trackEvent } from "@/services/matomo.js"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import AppSeparator from "@/components/AppSeparator.vue"

/* Store */
const store = useRootStore()

/* Ressources */
const ressources = [
  {
    download: true,
    href: "/static/documents/achats_fichier_exemple_ma_cantine.csv",
    name: "Télécharger notre fichier d’exemple CSV",
    size: "189 octets",
  },
  {
    external: true,
    name: "Comment importer un fichier CSV dans Excel ?",
  },
  {
    external: true,
    href:
      "https://support.microsoft.com/fr-fr/office/enregistrer-un-classeur-au-format-texte-txt-ou-csv-3e9a9d6c-70da-4255-aa28-fcacf1f081e6",
    name: "Comment enregistrer mon fichier Excel en CSV ?",
  },
]

/* Upload */
const isProcessingFile = ref(false)
const upload = (file) => {
  if (isProcessingFile.value) return
  isProcessingFile.value = true
  importPurchases({ file: file })
    .then((json) => {
      isProcessingFile.value = false
      const uploadedRows = json.count
      if (uploadedRows >= 1) {
        successUpload({ seconds: json.seconds, count: json.count })
      } else if (json.duplicateFile) {
        duplicatedUpload(json.duplicatePurchases)
      } else {
        alert("ERREUR")
      }
    })
    .catch((e) => {
      store.notifyServerError(e)
      isProcessingFile.value = false
    })
}

const importSuccess = ref(false)
const purchaseCount = ref(0)
const successUpload = (props) => {
  const { seconds, count } = props
  const message = `Fichier traité en ${Math.round(seconds)} secondes`
  store.notify({ message })
  purchaseCount.value = count
  importSuccess.value = true
  trackEvent({ category: "inquiry", action: "send", value: "import-purchases-success" })
}

const duplicatedUpload = (purchases) => {
  const countPurchases = purchases.length
  const description =
    countPurchases > 1
      ? `Ce fichier a déjà été utilisé pour importer ${countPurchases} achats :`
      : `Ce fichier a déjà été utilisé pour importer 1 achat :`
  hasErrors.list = [
    {
      description,
      purchases,
    },
  ]
  showErrors(1)
}

const hasErrors = reactive({
  status: false,
  badge: "",
  message: "",
  list: [],
})
const showErrors = (count) => {
  hasErrors.status = true
  hasErrors.badge = count > 1 ? `${count} Erreurs détectées` : "1 Erreur détectée"
  hasErrors.message =
    count > 1
      ? "Veuillez les corriger avant d’importer à nouveau le fichier."
      : "Veuillez la corriger avant d’importer à nouveau le fichier."
}
</script>

<template>
  <h1>Créer des achats</h1>
  <p class="fr-col-7">
    Notre outil d’import de masse vous permet d’ajouter les achats de toutes vos cantines d’un coup.
    <strong>Si vous avez moins de 10 achats,</strong>
    il est plus rapide de les saisir directement
    <router-link :to="{ name: 'PurchasesHome' }">sur la plateforme</router-link>
    .
  </p>
  <ImportExplanation :ressources="ressources" />
  <ImportSchemaTable
    url="https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/achats.json"
  />
  <section
    class="fr-px-6w fr-px-xl-9w fr-py-6w fr-background-alt--blue-france fr-mt-4w fr-grid-row fr-grid-row--middle"
  >
    <div class="fr-hidden fr-unhidden-xl fr-col-3 fr-pr-6w fr-grid-row--center">
      <img src="/static/pictos/document.svg" alt="" />
    </div>
    <div class="import-file-upload fr-col-12 fr-col-xl-9 fr-py-3w fr-px-4w fr-card">
      <DsfrFileUpload
        label="Avant d’importer votre fichier en CSV, assurez-vous que vos données respectent le format ci-dessus"
        hint="Extension du fichier autorisé : CSV"
        @change="upload"
        :disabled="isProcessingFile"
      />
      <div v-if="hasErrors.status" class="fr-mt-2w">
        <div class="fr-grid-row fr-grid-row--middle">
          <DsfrBadge type="error" :label="hasErrors.badge" />
          <p class="fr-text-default--error fr-ml-1w fr-mb-0">
            {{ hasErrors.message }}
          </p>
        </div>
        <AppSeparator class="fr-my-3w" />
        <ul>
          <li v-for="(error, index) in hasErrors.list" :key="index" class="fr-text-default--error">
            <p class="fr-mb-1v ma-cantine--bold">
              {{ error.description }}
            </p>
            <ul class="ma-cantine--unstyled-list fr-text-default--grey">
              <li v-for="(purchase, index) in error.purchases" :key="index">
                {{ purchase.description }} | {{ purchase.date }} | {{ purchase.priceHt }}€
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </section>
  <ImportSuccessModal
    :opened="importSuccess"
    :message="
      purchaseCount > 1
        ? 'Vos achats sont enregistrés et sont maintenant disponibles.'
        : 'Votre achat est enregistré et est maintenant disponible.'
    "
    @close="importSuccess = false"
  />
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
