<script setup>
defineProps(['label', 'value', 'tooltip'])
</script>

<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-mb-1w">
    <div class="fr-col-12 fr-col-md-5">
      <p class="fr-mb-0 fr-text--bold">{{ label }} :</p>
    </div>
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-0">
        {{ value }}
        <DsfrTooltip v-if="tooltip" :content="tooltip" />
      </p>
    </div>
  </div>
</template>
