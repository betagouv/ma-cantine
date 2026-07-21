<script setup>
import { ref, computed } from "vue"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"

const props = defineProps(["canteenId", "description"])
const store = useRootStore()
const descriptionInput = ref(props.description)
const descriptionInitial = ref(props.description)
const isSaving = ref(false)
const hasChanged = computed(() => descriptionInput.value !== descriptionInitial.value)

/* Save */
const saveDescription = () => {
  if (!descriptionInput.value) return
  isSaving.value = true
  canteenService.updateCanteen({ publicationComments: descriptionInput.value }, props.canteenId).then((response) => {
    if (!response?.id) store.notifyServerError(response)
    else successDescription(response)
  }).catch((error) => {
    store.notifyServerError(error)
  }).finally(() => {
    isSaving.value = false
  })
}

const successDescription = (response) => {
  descriptionInitial.value = response.publicationComments
  store.notify({
    title: "La description a été mise à jour",
    status: "success",
  })
}
</script>

<template>
  <div class="canteen-form-description">
    <h4 class="fr-h6 fr-mb-1w">Description de l'établissement</h4>
    <p class="fr-text--sm fr-mb-2w">En plus de rendre visible vos données EGalim, la description de votre établissement est la première brique de votre page publique, pour valoriser vos engagements et les actions de la cantine en faveur d’une alimentation durable et de qualité.</p>
    <DsfrInput
      v-model="descriptionInput"
      :isTextarea="true"
      label="Description"
      :label-visible="false"
      rows="4"
      hint="Optionnel"
      class="fr-mb-2w"
    />
    <DsfrButton
      v-if="hasChanged"
      label="Enregistrer la description de l'établissement"
      icon="ri-save-line"
      secondary
      :disabled="isSaving"
      @click="saveDescription"
    />
  </div>
</template>
