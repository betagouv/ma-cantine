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

const deleteImage = (imageId) => {
  isSaving.value = true
  canteenService.deleteCanteenImage(props.canteenId, imageId)
    .then(() => successImages("L'image a été supprimée"))
    .catch((error) => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
}

const updateAltImage = (imageId, altText) => {
  isSaving.value = true
  canteenService.updateCanteenImage(props.canteenId, imageId, { altText })
    .then((response) => {
      if (!response?.id) store.notifyServerError(response)
      else successImages("La description de l'image a été mise à jour")
    })
    .catch((error) => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
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
        @delete="deleteImage(image.id)"
        @save-alt="updateAltImage(image.id, $event)"
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
