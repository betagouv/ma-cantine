<script setup>
import { ref, computed } from "vue"
defineProps(["open"])
defineEmits(["close"])

/* Checkboxes */
const hasSiret = ref('')
const radioOptions = [
  {
    label: 'Oui',
    value: 'oui',
  },
  {
    label: 'Non',
    value: 'non',
  },
]

/* Search */
const search = ref('')
const numberName = computed(() => hasSiret.value === 'oui' ? "SIRET" : "SIREN")
</script>
<template>
  <DsfrModal :opened="open" title="Ajouter un restaurant satellite" @close="$emit('close')" size="lg">
    <p>Pour ajouter une cantine à votre groupe cette dernière doit : être enregistrée sur la plateforme, être de type "Restaurant satellite", ne doit pas déjà être associée à un groupe.</p>
    <DsfrRadioButtonSet
      v-model="hasSiret"
      legend="Le restaurant satellite a-t-il un numéro SIRET ?"
      :options="radioOptions"
      name="hasSiret"
      small
      inline
    />
    <DsfrSearchBar
      v-if="hasSiret"
      v-model="search"
      button-text="Rechercher"
      :placeholder="`Tapez le n° ${numberName} du restaurant satellite`"
      large
    />
  </DsfrModal>
</template>
