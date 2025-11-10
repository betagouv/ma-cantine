<script setup>
import { useRoute } from "vue-router"

const route = useRoute()
const pages = []
</script>

<template>
  <div>
    <h1>{{ route.meta.title }}</h1>
    <pre>{{ pages }}</pre>
  </div>
</template>
