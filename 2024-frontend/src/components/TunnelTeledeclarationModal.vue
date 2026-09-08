<script setup>
import { computed, ref } from 'vue'

const opened = defineModel(['opened'])
const emit = defineEmits(['close'])
const checkBoxeConfirmed = ref(false)
const modalActions = computed(() => [
  {
    label: 'Télédéclarer ces données',
    icon: 'ri-send-plane-line',
    disabled: !checkBoxeConfirmed.value,
    onClick: teledeclare,
  },
  {
    label: 'Annuler',
    secondary: true,
    onClick: closeModal,
  },
])

/* Actions */
const closeModal = () => {
  checkBoxeConfirmed.value = false
  emit('close')
}

const teledeclare = () => {
  console.log('teledeclare')
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
