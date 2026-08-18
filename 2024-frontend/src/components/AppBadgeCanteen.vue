<script setup>
import { computed } from "vue"

const props = defineProps(["canteen"])

const badge = computed(() => {
  const isGroupe = props.canteen?.isGroupe
  const isSatWithGroupe = props.canteen?.groupe !== null && props.canteen?.isSatellite
  if (isGroupe) return { type: "info", label: "Groupe" }
  else if (isSatWithGroupe) return { type: "new", label: "Cantine en gestion groupée" }
  return { type: "success", label: "Cantine" }
})
</script>

<template>
  <DsfrBadge :label="badge.label" :type="badge.type" :noIcon="true" />
</template>
