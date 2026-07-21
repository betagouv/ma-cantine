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
const saveLogo = async (file) => {
  if (!file) return
  const base64 = await toBase64(file)
  await updateLogo(base64)
}

const deleteLogo = () => updateLogo(null)

/* Update */
const updateLogo = async (value) => {
  isSaving.value = true
  try {
    const response = await canteenService.updateCanteen({ logo: value }, props.canteenId)
    if (!response?.id) store.notifyServerError(response)
    else successLogo(response)
  } catch (error) {
    store.notifyServerError(error)
  } finally {
    isSaving.value = false
  }
}

const successLogo = (response) => {
  displayLogo.value = response.logo
  store.notify({
    title: "Le logo a été mis à jour",
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
      @save-file="saveLogo"
    />
  </li>
</template>
