<script setup>
import { ref, computed, useId } from "vue"

const props = defineProps(["src", "alt", "disabled", "showAlt"])
const emit = defineEmits(["delete", "saveFile", "saveAlt"])

/* Input file */
const fileInputId = useId()
const fileInput = ref(null)
const file = ref(null)

const selectFile = () => {
  fileInput.value?.click()
}

const onFileChange = (event) => {
  file.value = event.target.files?.[0] || null
  if (file.value) saveFile()
  event.target.value = ""
}

/* Alt Input */
const altInput = ref(props.alt || "")
const altInitial = computed(() => props.alt || "")
const altChanged = computed(() => altInitial.value !== altInput.value)

/* Save */
const saveFile = () => {
  emit("saveFile", file.value)
}

const saveAlt = () => {
  emit("saveAlt", altInput.value)
}

const deleteImage = () => {
  file.value = null
  emit("delete")
}
</script>

<template>
  <div class="app-form-image">
    <div v-if="src" class="fr-card fr-p-1w">
      <img class="app-form-image__image fr-background-alt--grey" :src="src" :alt="alt" />
      <div v-if="showAlt" class="fr-mt-2w">
        <DsfrInput
          v-model="altInput"
          :isTextarea="true"
          label="Description de l'image"
          label-visible
          hint="Optionnel - Cette description permet de fournir aux personnes malvoyantes une alternative textuelle à l'image. Si cette dernière contient du texte, pensez à le répéter ici."
        />
        <DsfrButton
          v-if="altChanged"
          label="Enregistrer la description"
          class="fr-mt-1w"
          secondary
          icon="fr-icon-save-line"
          :disabled="disabled"
          @click="saveAlt"
        />
      </div>
      <DsfrButton
        v-if="src"
        class="app-form-image__delete fr-background-default--grey"
        icon="fr-icon-delete-line"
        label="Supprimer"
        secondary
        :icon-only="true"
        :disabled="disabled"
        @click="deleteImage"
      />
    </div>
    <DsfrButton
      v-else
      label="Ajouter une image"
      secondary
      icon="ri-image-add-line"
      :disabled="disabled"
      @click="selectFile"
    />
    <label :for="fileInputId" class="fr-hidden">
      Ajouter une image
      <input
        :id="fileInputId"
        ref="fileInput"
        type="file"
        hidden
        accept="image/*"
        @change="onFileChange"
      />
    </label>
  </div>
</template>

<style scoped lang="scss">
.app-form-image {
  position: relative;

  &__image {
    display: block;
    width: 100%;
    height: 35vh;
    object-fit: contain;
  }
  &__delete {
    position: absolute;
    top: 0rem;
    right: 0rem;
  }
}
</style>
