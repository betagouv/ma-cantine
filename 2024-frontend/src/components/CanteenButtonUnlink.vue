<script setup>
import { ref } from "vue"
const props = defineProps(["canteen", "satellite"])
const loading = ref(false)
console.log(props.canteen, props.satellite)
</script>

<template>
  <DsfrButton
    secondary
    label="Retirer de mes satellites"
    :disabled="loading"
    icon="fr-icon-close-line"
    class="canteen-button-unlink"
  />
</template>

<style lang="scss">
.canteen-button-unlink {
  color: var(--text-action-high-red-marianne) !important;
  box-shadow: inset 0 0 0 1px var(--text-action-high-red-marianne) !important;
}
</style>
