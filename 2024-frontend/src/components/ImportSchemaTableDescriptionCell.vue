<script setup>
const cell = defineProps(["title", "description", "constraints", "multiple", "separator"])
</script>

<template>
  <p class="fr-text--sm fr-mb-1w">{{ cell.title }}</p>
  <p v-if="cell.description" class="fr-text--sm">{{ cell.description }}</p>
  <p v-if="cell.constraints" class="fr-text--sm">
    <span>Options acceptées :&#32;</span>
    <span v-for="(item, idx) in cell.constraints" :key="idx">
      <code class="fr-background-contrast--blue-france fr-px-1v">{{ item }}</code>
      <span v-if="idx < cell.constraints.length - 1">,&#32;</span>
    </span>
  </p>
  <p v-if="cell.multiple" class="fr-text--sm">
    Spécifiez plusieurs options en séparant avec un
    <code class="fr-background-contrast--blue-france fr-px-1v">{{ cell.separator }}</code>
  </p>
</template>
