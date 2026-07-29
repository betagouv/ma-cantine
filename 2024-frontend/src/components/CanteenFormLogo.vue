<script setup>
import { ref, watch } from "vue"
import { toBase64 } from "@/utils.js"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import AppFormImage from "@/components/AppFormImage.vue"

const props = defineProps(["canteenId", "logo"])
const store = useRootStore()
const displayLogo = ref(props.logo || null)
const isSaving = ref(false)

/* Logo change */
watch( () => props.logo, (newLogo) => {
  displayLogo.value = newLogo || null
})

/* Actions */
const addLogo = async (file) => {
  if (!file) return
  const base64 = await toBase64(file)
  isSaving.value = true
  canteenService.addCanteenLogo(props.canteenId, base64)
    .then(response => {
      if (!response?.id) store.notifyServerError(response)
      else successLogo(response.logo)
    })
    .catch(error => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
}

const deleteLogo = async () => {
  isSaving.value = true
  canteenService.deleteCanteenLogo(props.canteenId)
    .then(() => successLogo(null))
    .catch(error => store.notifyServerError(error))
    .finally(() => { isSaving.value = false })
}

const successLogo = (logo) => {
  displayLogo.value = logo
  const message = logo ? "Le logo a été mis à jour" : "Le logo a été supprimé"
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
      :src="displayLogo"
      :disabled="isSaving"
      @delete="deleteLogo"
      @save-file="addLogo"
    />
  </li>
</template>
