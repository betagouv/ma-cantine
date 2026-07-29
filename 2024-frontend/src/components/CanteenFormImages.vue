<script setup>
import { ref, onMounted } from "vue"
import { toBase64 } from "@/utils.js"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import AppFormImage from "@/components/AppFormImage.vue"

const props = defineProps(["canteenId"])
const store = useRootStore()
const isSaving = ref(false)
const canteenImages = ref([])

/* Display images */
const setImages = async () => {
  const response = await canteenService.fetchCanteenImages(props.canteenId)
  canteenImages.value = response
}
onMounted(setImages)

/* Actions */
const addImage = async (file) => {
  if (!file) return
  const base64 = await toBase64(file)
  isSaving.value = true
  canteenService.addCanteenImage(props.canteenId, base64)
    .then((response) => {
      if (!response?.id) store.notifyServerError(response)
      else successImages("L'image a été ajoutée")
    })
    .catch((error) => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
}

const deleteImage = (imageToDelete) => {
  const nextImages = canteenImages.value.filter((image) => image.image !== imageToDelete.image)
  updateImages(nextImages)
}

const saveAlt = (imageToSave, altText) => {
  const imageIndex = canteenImages.value.findIndex((image) => image.image === imageToSave.image)
  canteenImages.value[imageIndex].altText = altText
  updateImages(canteenImages.value)
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

const successImages = (message) => {
  setImages()
  store.notify({
    title: message,
    status: "success",
  })
}
</script>

<template>
  <li class="canteen-form-images">
    <h4 class="fr-h6 fr-mb-1w">Images de l'établissement</h4>
    <div class="fr-grid-row fr-grid-row--gutters">
      <AppFormImage
        v-for="image in canteenImages"
        :key="image.id"
        :src="image.image"
        :alt="image.altText"
        :disabled="isSaving"
        :show-alt="true"
        @delete="deleteImage(image)"
        @save-alt="saveAlt(image, $event)"
        class="fr-col-12 fr-col-md-4"
      />
      <AppFormImage
        :disabled="isSaving"
        class="fr-col-12 fr-col-md-4"
        @save-file="addImage"
      />
    </div>
  </li>
</template>
