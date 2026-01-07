<script setup>
import { ref } from "vue"
defineProps(["open"])
defineEmits(["close"])
const hasSiret = ref(false)
const radioOptions = [
  {
    label: 'Oui',
    value: '1',
  },
  {
    label: 'Non',
    value: '0',
  },
]
</script>
<template>
  <DsfrModal :opened="open" title="Ajouter un restaurant satellite" @close="$emit('close')" size="lg">
    <p>Pour ajouter une cantine à votre groupe cette dernière doit : être enregistrée sur la plateforme, être de type "Restaurant satellite", ne doit pas déjà être associée à un groupe.</p>
    <DsfrRadioButtonSet
      legend="Le restaurant satellite a-t-il un numéro SIRET ?"
      :modelValue="hasSiret"
      :options="radioOptions"
      name="hasSiret"
      small
      inline
    />
  </DsfrModal>
</template>
