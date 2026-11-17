<script setup>
import IconMacaronBase from "@/components/IconMacaronBase.vue"
import diagnosticsMacaron from "@/services/diagnosticsMacaron.js"

const color = diagnosticsMacaron.getColor("cantine")
</script>

<template>
  <IconMacaronBase :color="color" />
</template>
