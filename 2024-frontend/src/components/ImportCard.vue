<script setup>
defineProps(["title", "description", "icon"])
</script>
<template>
  <div class="fr-card fr-p-4w">
    <div>
      <img :src="icon" :alt="`Illustration de ${title}`">
      <h2 class="fr-h5">{{ title }}</h2>
      <p>{{ description }}</p>
    </div>
    <div>
      <slot></slot>
    </div>
  </div>
</template>
