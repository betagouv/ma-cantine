<script setup>
import { ref, useId } from "vue"

defineProps(["src", "alt", "disabled", "showEdit", "emptyMessage"])
const emit = defineEmits(["delete", "change"])

/* File */
const inputId = useId()
const fileInput = ref(null)
const selectFile = () => {
  fileInput.value?.click()
}
</script>

<template>
  <div class="app-form-image fr-card fr-p-1w">
    <div v-if="src" class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <img :src="src" :alt="alt" class="app-form-image__image" />
      </div>

      <div class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--middle fr-grid-row--center">
        <DsfrButton
          v-if="showEdit"
          label="Modifier"
          secondary
          icon="ri-pencil-line"
          :disabled="disabled"
          @click="selectFile"
          class="fr-mr-1w"
        />
        <DsfrButton
          label="Supprimer"
          tertiary
          icon="fr-icon-delete-line"
          :disabled="disabled"
          @click="emit('delete')"
        />
      </div>
    </div>

    <div v-else class="ma-cantine--flex-center ma-cantine--flex-column fr-p-3w">
      <p>{{ emptyMessage }}</p>
      <DsfrButton
        label="Ajouter"
        tertiary
        icon="ri-image-add-line"
        :disabled="disabled"
        @click="selectFile"
      />
    </div>

    <label class="fr-hidden" :for="inputId">
      Ajouter une image
      <input
        :id="inputId"
        ref="fileInput"
        type="file"
        accept="image/*"
        @change="emit('change', $event)"
      />
    </label>
  </div>
</template>

<style scoped>
.app-form-image__image {
  display: block;
  width: 100%;
  max-height: 50vh;
  object-fit: contain;
}
</style>
