<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import { importPurchases } from "@/services/imports.js"
import { trackEvent } from "@/services/matomo.js"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"

/* Store and Router */
const store = useRootStore()
const router = useRouter()

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
      } else {
        alert("ERREUR")
      }
    })
    .catch((e) => {
      store.notifyServerError(e)
      isProcessingFile.value = false
    })
}

const modalOpened = ref(false)
const purchaseCount = ref(0)
const successUpload = (props) => {
  const { seconds, count } = props
  const message = `Fichier traité en ${Math.round(seconds)} secondes`
  store.notify({ message })
  purchaseCount.value = count
  modalOpened.value = true
  trackEvent({ category: "inquiry", action: "send", value: "import-purchases-success" })
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
    </div>
  </section>
  <DsfrModal
    :opened="modalOpened"
    class="fr-modal--opened"
    title="Le fichier a été importé avec succès"
    icon="fr-icon-checkbox-circle-fill"
    @close="modalOpened = false"
    :actions="[
      {
        label: 'Aller sur mon tableau de bord',
        onClick() {
          router.push({ name: 'ManagementPage' })
        },
      },
    ]"
  >
    <template #default>
      <p class="ma-cantine--bold">
        {{
          purchaseCount > 1
            ? "Vos achats sont enregistrés et sont maintenant disponibles."
            : "Votre achat est enregistré et est maintenant disponible."
        }}
      </p>
      <p>
        Depuis votre tableau de bord, vous devez télédéclarer vos données, lorsque la campagne de télédéclaration est
        ouverte.
      </p>
    </template>
  </DsfrModal>
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
