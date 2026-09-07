<script setup>
import { computed } from 'vue'

const props = defineProps(["errors"])
const badge = computed(() => {
  const count = props.errors.length
  const sentence = count > 1 ? 'erreurs détectées' : 'erreur détectée'
  return `${count} ${sentence}`
})
</script>

<template>
  <DsfrBadge :label="badge" type="error" />
  <ul>
    <li v-for="field in errors" :key="field" class="fr-text-default--error">
      <p class="fr-mb-0">
        erreur sur le champ <span class="ma-cantine--bold">« {{ field }} »</span>
      </p>
    </li>
  </ul>
</template>
