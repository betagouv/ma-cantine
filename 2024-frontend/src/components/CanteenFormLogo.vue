<script setup>
import { computed, ref, watch } from "vue"
import { toBase64 } from "@/utils.js"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"

const props = defineProps(["canteen"])
const store = useRootStore()
const fileInput = ref(null)
const logo = ref(props.canteen.logo || null)
const hasLogo = computed(() => logo.value !== null)
const isSaving = ref(false)

/* Canteen change */
watch(props.canteen, (newCanteen) => {
  logo.value = newCanteen.logo || null
})

/* File input */
const selectFile = () => {
  fileInput.value?.click()
}

const onFileChange = async (event) => {
  const file = event.target.files?.[0]
  event.target.value = ""
  if (!file) return
  const base64 = await toBase64(file)
  await updateLogo(base64)
}

/* Actions */
const deleteLogo = () => updateLogo(null)

const updateLogo = async (value) => {
  isSaving.value = true
  try {
    const response = await canteenService.updateCanteen({ logo: value }, props.canteen.id)
    if (!response?.id) store.notifyServerError(response)
    else successLogo(response)
  } catch (error) {
    store.notifyServerError(error)
  } finally {
    isSaving.value = false
  }
}

const successLogo = (response) => {
  logo.value = response.logo
  store.notify({
    title: "Le logo a été mis à jour",
    status: "success",
  })
}
</script>

<template>
  <div class="canteen-form-logo">
    <h4 class="fr-h6 fr-mb-2w">Logo de l'établissement</h4>

    <div v-if="hasLogo" class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom">
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card fr-p-1w">
          <img :src="logo" alt="Logo de l'établissement" class="canteen-form-logo__image" />
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrButton
          label="Modifier le logo"
          secondary
          icon="ri-pencil-line"
          :disabled="isSaving"
          @click="selectFile"
          class="fr-mb-1w"
        />
        <br/>
        <DsfrButton
          label="Supprimer le logo"
          tertiary
          icon="fr-icon-delete-line"
          :disabled="isSaving"
          @click="deleteLogo"
        />
      </div>
    </div>
    <div v-else>
      <p>Vous n'avez pas encore ajouté de logo pour votre établissement.</p>
      <DsfrButton
        label="Ajouter un logo"
        tertiary
        icon="ri-image-add-line"
        :disabled="isSaving"
        @click="selectFile"
      />
    </div>

    <label class="fr-hidden" for="canteen-form-logo-input">
      Ajouter une image pour le logo de l'établissement
      <input
        id="canteen-form-logo-input"
        ref="fileInput"
        type="file"
        accept="image/*"
        @change="onFileChange"
      />
    </label>
  </div>
</template>

<style scoped>
.canteen-form-logo__image {
  display: block;
  width: 100%;
  max-height: 35vh;
  object-fit: contain;
}
</style>
