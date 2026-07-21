<script setup>
import { ref } from "vue"

const props = defineProps(["src", "alt", "disabled"])
const emit = defineEmits(["delete", "save"])
const fileInput = ref("")
const file = ref(null)

const updateFile = (files) => {
  file.value = files?.[0] || null
  if (!props.alt) emit("save", file.value)
}

const save = () => {
  if (!file.value) return
  emit("save", file.value)
  file.value = null
  fileInput.value = ""
}
</script>

<template>
  <div class="app-form-image fr-card fr-p-1w">
    <img v-if="src" class="app-form-image__image fr-background-alt--grey" :src="src" :alt="alt" />
    <DsfrFileUpload
      v-if="!src"
      v-model="fileInput"
      label="Télécharger une image"
      accept="image/*"
      @change="updateFile"
    />
    <DsfrButton
      v-if="alt"
      label="Enregistrer l'image"
      class="fr-mt-2w"
      secondary
      icon="fr-icon-save-line"
      :disabled="disabled || !file"
      @click="save"
    />
    <DsfrButton
      v-if="src"
      class="app-form-image__delete fr-background-default--grey"
      icon="fr-icon-delete-line"
      label="Supprimer"
      secondary
      size="sm"
      :icon-only="true"
      :disabled="disabled"
      @click="emit('delete')"
    />
  </div>
</template>

<style scoped lang="scss">
.app-form-image {
  position: relative;

  &__image {
    display: block;
    width: 100%;
    max-height: 35vh;
    object-fit: contain;
  }
  &__delete {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
  }
}
</style>
