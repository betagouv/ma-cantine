<script setup>
import { useRoute } from "vue-router"
const route = useRoute()
</script>

<template>
  <section>
    <h1>{{ route.meta.title }}</h1>
  </section>
</template>
