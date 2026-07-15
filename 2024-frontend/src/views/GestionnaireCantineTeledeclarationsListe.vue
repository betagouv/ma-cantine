<script setup>
import { useRoute } from "vue-router"
import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"

const route = useRoute()
</script>

<template>
  <LayoutSidebarCanteen>
    <template #titleName>
      <h2 class="fr-h3 fr-mb-0">{{ route.meta.title }}</h2>
    </template>
  </LayoutSidebarCanteen>
</template>
