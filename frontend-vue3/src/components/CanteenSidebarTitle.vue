<script setup>
import AppSeparator from "@/components/AppSeparator.vue"
defineProps(["title"])
</script>

<template>
  <div class="canteen-sidebar-title">
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mt-2w fr-mt-md-0 fr-mb-2w fr-mb-md-0">
      <h2 class="fr-h3 fr-mb-0">{{ title }}</h2>
      <slot />
    </div>
    <AppSeparator class="canteen-sidebar-title__separator fr-mt-3w fr-mb-5w" />
  </div>
</template>

<style lang="scss">
.canteen-sidebar-title {
  &__separator {
    display: none;

    @media (min-width: 768px) {
      display: block;
    }
  }
}
</style>
