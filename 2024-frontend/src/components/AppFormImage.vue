<script setup>
import { ref, computed } from "vue"

const props = defineProps(["src", "alt", "disabled", "showAlt"])
const emit = defineEmits(["delete", "save"])

/* Input file */
const fileInput = ref("")
const file = ref(null)
const updateFile = (files) => {
  file.value = files?.[0] || null
  if (!props.alt) saveFile()
}

/* Alt Input */
const altInput = ref(props.alt || "")
const altInitial = computed(() => props.alt || "")
const altChanged = computed(() => altInitial.value !== altInput.value)

/* Save */
const saveFile = () => {
  emit("save", file.value)
}

const saveAlt = () => {
  emit("saveAlt", altInput.value)
}
</script>

<template>
  <div class="app-form-image fr-card fr-p-1w">
    <img v-if="src" class="app-form-image__image fr-background-alt--grey" :src="src" :alt="alt" />
    <DsfrFileUpload
      v-else
      v-model="fileInput"
      label="Télécharger une image"
      accept="image/*"
      @change="updateFile"
    />
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
