<script setup>
defineProps(["image", "title", "color"])
</script>

<template>
  <div class="observatory-graph-card-title">
    <div class="fr-grid-row fr-grid-row--middle">
      <img :src="image" class="observatory-graph-card-title__image" alt="" />
      <h2 class="observatory-graph-card-title fr-ml-3w fr-h5 fr-mb-0" :style="`color: ${color}`">
        {{ title }}
      </h2>
    </div>
    <p class="fr-pl-9w fr-col-8">
      <slot></slot>
    </p>
  </div>
</template>

<style lang="scss">
.observatory-graph-card-title {
  &__image {
    width: 3rem;
    height: 3rem;
  }
}
</style>
