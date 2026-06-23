<script setup>
defineProps(["title", "description", "icon"])
</script>
<template>
  <div class="fr-card fr-p-4w">
    <div>
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle fr-grid-row--left fr-mb-2w">
        <img :src="icon" :alt="`Illustration de ${title}`">
        <h2 class="fr-h5 fr-text-title--blue-france fr-mb-0 fr-ml-2w">{{ title }}</h2>
      </div>
      <p>{{ description }}</p>
      <slot></slot>
    </div>
  </div>
</template>
