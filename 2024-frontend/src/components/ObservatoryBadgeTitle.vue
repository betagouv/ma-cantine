<script setup>
defineProps(["image", "title", "color"])
</script>

<template>
  <div class="observatory-badge-title">
    <div class="observatory-badge-title__top fr-mb-2w">
      <img :src="image" class="observatory-badge-title__image" alt="" />
      <h2 class="fr-h4 fr-mt-2w fr-mt-md-0 fr-ml-md-4w fr-mb-0" :style="`color: ${color}`">
        {{ title }}
      </h2>
    </div>
    <p class="fr-pl-md-10w fr-col-12 fr-col-md-10 fr-mb-0">
      <slot></slot>
    </p>
  </div>
</template>

<style lang="scss">
.observatory-badge-title {

  &__top {
    display: flex;
    flex-direction: column;

    @media (min-width: 768px) {
      flex-direction: row;
      align-items: center;
    }
  }

  &__image {
    width: 3rem;
    height: 3rem;
    flex-shrink: 0;
  }
}
</style>
