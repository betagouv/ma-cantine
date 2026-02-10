<script setup>
import { ref } from "vue"
import canteenService from "@/services/canteens"
import AppLoader from "@/components/AppLoader.vue"

/* PROPS and EMITS */
defineProps(["opened"])
const emit = defineEmits(["close"])

/* EXPORT */
const isGenerating = ref(false)
const exportSucces = ref(false)
const exportError = ref(null)

const generateExport = () => {
  isGenerating.value = true
  canteenService.exportCanteens()
    .then(() => exportSucces.value = true)
    .catch(() => exportError.value = true)
    .finally(() => isGenerating.value = false)
}

/* MODAL */
const closeModal = () => {
  isGenerating.value = false
  exportSucces.value = false
  exportError.value = null
  emit('close')
}
</script>

<template>
  <DsfrModal
    :opened="opened"
    title="Export des informations de mes cantines"
    @close="closeModal"
  >
    <p>
      Cet export contient l'ensemble des données d’information relatives aux cantines dont vous gérez.
      Vous pourrez modifier ce fichier et le ré-utiliser tel quel dans le module d’import “Modifier des cantines” pour mettre à jour vos informations en masse.
    </p>
    <DsfrHighlight text="Pour rappel, pour modifier les cantines via imports ou créer des bilans, vous devez être gestionnaire de celles-ci." class="fr-ml-0"/>
    <DsfrAlert v-if="exportSucces" type="success" title="L'export a été généré avec succès." description="Vous pouvez le retrouver dans vos téléchargements." />
    <DsfrAlert v-else-if="exportError" type="error" title="Une erreur est survenue lors de la génération de l'export." description="Veuillez réessayer plus tard ou contacter le support." />
    <div v-else class="fr-grid-row fr-grid-row--left fr-grid-row--middle">
      <DsfrButton primary label="Générer l'export" :disabled="isGenerating" @click="generateExport" />
      <AppLoader text="Génération de l'export en cours" v-if="isGenerating" class="fr-ml-2w" />
    </div>
  </DsfrModal>
</template>
