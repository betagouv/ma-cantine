<script setup>
import { ref, onMounted } from "vue"
import { toBase64 } from "@/utils.js"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import AppFormImage from "@/components/AppFormImage.vue"

const props = defineProps(["canteenId"])
const store = useRootStore()
const isSaving = ref(false)
const logoUrl = ref(null)

/* Display logo */
const setLogoUrl = async () => {
  canteenService.fetchCanteenLogo(props.canteenId)
    .then(response => logoUrl.value = response.logo)
    .catch(error => store.notifyServerError(error))
}
onMounted(setLogoUrl)

/* Actions */
const addLogo = async (file) => {
  if (!file) return
  const base64 = await toBase64(file)
  isSaving.value = true
  canteenService.addCanteenLogo(props.canteenId, base64)
    .then(response => {
      if (!response?.id) store.notifyServerError(response)
      else successLogo("Le logo a été mis à jour")
    })
    .catch(error => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
}

const deleteLogo = async () => {
  isSaving.value = true
  canteenService.deleteCanteenLogo(props.canteenId)
    .then(() => successLogo("Le logo a été supprimé"))
    .catch(error => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
}

/* Success */
const successLogo = (message) => {
  setLogoUrl()
  store.notify({
    title: message,
    status: "success",
  })
}
</script>

<template>
  <li class="canteen-form-logo">
    <h4 class="fr-h6 fr-mb-2w">Logo de l'établissement</h4>
    <AppFormImage
      :src="logoUrl"
      :disabled="isSaving"
      @delete="deleteLogo"
      @save-file="addLogo"
    />
  </li>
</template>
