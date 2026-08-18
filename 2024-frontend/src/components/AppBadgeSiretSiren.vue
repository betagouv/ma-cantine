<script setup>
import { computed } from "vue"
import { formatSiretOrSiren } from "@/utils"

const props = defineProps(["canteen"])

const label = computed(() => {
  const hasSiret = props.canteen?.siret
  const name = hasSiret ? "SIRET" : "SIREN"
  const valueToFormat = hasSiret ? props.canteen.siret : props.canteen.sirenUniteLegale
  return `${name} : ${formatSiretOrSiren(valueToFormat)}`
})
</script>

<template>
  <DsfrBadge :label="label" type="neutral" />
</template>
