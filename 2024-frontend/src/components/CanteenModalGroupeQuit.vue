<script setup>
import { ref } from "vue"
import { useStoreCanteen } from "@/stores/canteen.js"
import canteensService from "@/services/canteens"

const props = defineProps(["opened", "canteen"])
const emit = defineEmits(["close"])
const canteenStore = useStoreCanteen()
const loading = ref(false)
const errorMessage = ref(null)

const close = () => {
  errorMessage.value = null
  emit("close")
}

const quitGroupe = () => {
  loading.value = true
  canteensService
    .unlinkSatellite(props.canteen.groupe.id, props.canteen.id)
    .then(async (response) => {
      if (response?.status === "error") {
        errorMessage.value = response.message
        return
      }
      canteenStore.refreshStore()
      await canteenStore.initStore(props.canteen.id)
      close()
    })
    .finally(() => {
      loading.value = false
    })
}
</script>

<template>
  <DsfrModal
    :opened="opened"
    title="Souhaitez-vous quitter le groupe ?"
    @close="close"
  >
    <p>
      En quittant le groupe vous vous engager à en rejoindre un autre ou à déclarer vos achats par vos propres moyens.
    </p>
    <p class="fr-text--bold">Confirmez-vous votre demande ?</p>
    <p v-if="errorMessage" class="fr-error-text fr-mb-0">{{ errorMessage }}</p>
    <div v-else class="ma-cantine--flex-end">
      <DsfrButton
        secondary
        label="Annuler"
        :disabled="loading"
        @click="close"
      />
      <DsfrButton
        primary
        label="Valider"
        :disabled="loading"
        @click="quitGroupe"
      />
    </div>
  </DsfrModal>
</template>
