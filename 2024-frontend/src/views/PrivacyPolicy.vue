<script setup>
import { useRoute } from "vue-router"
const route = useRoute()
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
</template>
