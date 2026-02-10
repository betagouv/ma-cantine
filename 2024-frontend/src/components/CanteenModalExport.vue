<script setup>
import { ref } from "vue"
import AppLoader from "@/components/AppLoader.vue"

defineProps(["opened"])
const emit = defineEmits(["close"])
const isGenerating = ref(false)

/* EXPORT */
const generateExport = () => {
  isGenerating.value = true
}

/* MODAL */
const closeModal = () => {
  isGenerating.value = false
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
    <div class="fr-grid-row fr-grid-row--left fr-grid-row--middle">
      <DsfrButton primary label="Générer l'export" :disabled="isGenerating" @click="generateExport" />
      <AppLoader text="Génération de l'export en cours" v-if="isGenerating" class="fr-ml-2w" />
    </div>
  </DsfrModal>
</template>
