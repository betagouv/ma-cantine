<script setup>
import { ref, useId } from "vue"

defineProps(["src", "alt", "disabled"])
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
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div>
          <img v-if="src" :src="src" :alt="alt" class="app-form-image__image" />
          <DsfrButton
            v-else
            label="Ajouter"
            tertiary
            icon="ri-image-add-line"
            :disabled="disabled"
            @click="selectFile"
          />
        </div>
      </div>

      <div v-if="src" class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--middle">
        <DsfrButton
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
  max-height: 35vh;
  object-fit: contain;
}
</style>
