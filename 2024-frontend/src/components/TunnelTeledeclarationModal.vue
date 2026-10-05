<script setup>
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useRootStore } from '@/stores/root'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import diagnosticServices from '@/services/diagnostics'

const opened = defineModel(['opened'])
const emit = defineEmits(['close'])
const rootStore = useRootStore()
const router = useRouter()

/* Teledeclaration */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)

/* Modale */
const checkBoxeConfirmed = ref(false)
const loading = ref(false)
const modalActions = computed(() => [
  {
    label: loading.value ? 'Télédéclaration en cours...' : 'Télédéclarer ces données',
    icon: 'ri-send-plane-line',
    disabled: !checkBoxeConfirmed.value || loading.value,
    onClick: teledeclare,
  },
  {
    label: 'Annuler',
    secondary: true,
    onClick: closeModal,
  },
])

const closeModal = () => {
  checkBoxeConfirmed.value = false
  loading.value = false
  emit('close')
}

/* Teledeclare */
const teledeclare = () => {
  if (!diagnostic.value) return
  loading.value = true
  diagnosticServices
    .teledeclareDiagnostic(diagnostic.value.canteenId, diagnostic.value.id)
    .then((response) => {
      if (response?.status === 'error' || response instanceof Error) displayError(response)
      else router.push({ name: 'GestionnaireTunnelApproTeledeclares' })
    })
    .catch((e) =>  displayError(e))
    .finally(() => {
      loading.value = false
    })
}

const displayError = (error) => {
  rootStore.notifyServerError(error)
  loading.value = false
}
</script>

<template>
  <DsfrModal
    :opened="opened"
    title="Plus qu’une étape vous valider votre déclaration"
    @close="closeModal"
    :actions="modalActions"
  >
    <p>
      Retrouver votre justificatif de déclaration et la synthèse de votre qualité de produits dans votre espace cantine.
    </p>
    <DsfrCheckbox
      v-model="checkBoxeConfirmed"
      name="checkBoxeConfirmed"
      label="Je déclare sur l'honneur la véracité de ces informations"
    />
  </DsfrModal>
</template>
