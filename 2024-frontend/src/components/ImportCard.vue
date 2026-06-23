<script setup>
import AppSeparator from "@/components/AppSeparator.vue"
defineProps(["title", "description", "icon"])
</script>
<template>
  <div class="fr-card fr-p-4w">
    <div>
      <img :src="icon" :alt="`Illustration de ${title}`">
      <h2 class="fr-h5 fr-text-title--blue-france">{{ title }}</h2>
      <p class="fr-mb-0">{{ description }}</p>
    </div>
    <AppSeparator class="fr-my-3w" />
    <div>
      <slot></slot>
    </div>
  </div>
</template>
