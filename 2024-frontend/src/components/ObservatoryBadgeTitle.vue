<script setup>
defineProps(["image", "title", "color"])
</script>

<template>
  <div class="observatory-badge-title">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <img :src="image" class="observatory-badge-title__image" alt="" />
      <h2 class="observatory-badge-title fr-ml-4w fr-h4 fr-mb-0" :style="`color: ${color}`">
        {{ title }}
      </h2>
    </div>
    <p class="fr-pl-10w fr-col-12 fr-col-md-10 fr-mb-0">
      <slot></slot>
    </p>
  </div>
</template>

<style lang="scss">
.observatory-badge-title {
  &__image {
    width: 3rem;
    height: 3rem;
  }
}
</style>
