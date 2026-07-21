<script setup>
import { computed, ref, watch } from "vue"
import { toBase64 } from "@/utils.js"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import AppFormImage from "@/components/AppFormImage.vue"

const props = defineProps(["canteenId", "images"])
const store = useRootStore()
const displayImages = ref(props.images || [])
const isSaving = ref(false)
const maxImages = 3
const canAddImage = computed(() => displayImages.value.length < maxImages)

/* Images change */
watch(() => props.images, (newImages) => {
  displayImages.value = newImages || []
})

/* Actions */
const saveImage = async (file) => {
  if (!file || !canAddImage.value) return
  const base64 = await toBase64(file)
  await updateImages([...displayImages.value, { image: base64 }])
}

const deleteImage = (imageToDelete) => {
  const nextImages = displayImages.value.filter((image) => image.image !== imageToDelete.image)
  updateImages(nextImages)
}

const saveAlt = (imageToSave, altText) => {
  const imageIndex = displayImages.value.findIndex((image) => image.image === imageToSave.image)
  displayImages.value[imageIndex].altText = altText
  updateImages(displayImages.value)
}

const updateImages = async (value) => {
  isSaving.value = true
  try {
    const response = await canteenService.updateCanteen({ images: value }, props.canteenId)
    if (!response?.id) store.notifyServerError(response)
    else successImages(response)
  } catch (error) {
    store.notifyServerError(error)
  } finally {
    isSaving.value = false
  }
}

const successImages = (response) => {
  displayImages.value = response.images || []
  store.notify({
    title: "L'image a été mise à jour",
    status: "success",
  })
}
</script>

<template>
  <div class="canteen-form-images">
    <h4 class="fr-h6 fr-mb-1w">Images de l'établissement</h4>
    <p class="fr-text--sm fr-mb-2w">Vous pouvez ajouter jusqu'à 3 images.</p>

    <AppFormImage
      v-for="image in displayImages"
      :key="image.image"
      :src="image.image"
      :alt="image.altText"
      :disabled="isSaving"
      :show-alt="true"
      class="fr-mb-2w"
      @delete="deleteImage(image)"
      @save-alt="saveAlt(image, $event)"
    />

    <AppFormImage
      v-if="canAddImage"
      :disabled="isSaving"
      @save="saveImage"
    />
  </div>
</template>
