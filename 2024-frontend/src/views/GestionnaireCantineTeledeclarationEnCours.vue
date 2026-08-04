<script setup>
import { useRoute } from "vue-router"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"

const route = useRoute()
</script>

<template>
  <CanteenSidebarTitle :title="route.meta.title" />
</template>
