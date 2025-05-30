<script setup>
import { useRoute } from "vue-router"
const route = useRoute()
</script>

<template>
  <div class="fr-col-12 fr-col-lg-7 layout-one-column">
    <h1 class="fr-my-8w">{{ route.meta.title }}</h1>
    <slot></slot>
  </div>
</template>

<style lang="scss">
.layout-one-column {
  section {
    margin-top: 2rem;
  }
}
</style>
