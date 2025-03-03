<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import AppCode from "@/components/AppCode.vue"

defineOptions({ inheritAttrs: false })
const route = useRoute()
const props = defineProps(["id", "title", "description", "constraints", "multiple", "separator"])
const isSelected = computed(() => {
  const hash = route.hash.replace("#", "")
  return hash === props.id
})
const forAdmin = computed(() => props.id.startsWith("admin_"))
</script>

<template>
  <p
    :id
    class="fr-text--sm fr-mb-1w"
    :class="{
      selected: isSelected,
      admin: forAdmin,
    }"
  >
    {{ title }}
  </p>
  <p v-if="description" class="fr-text--sm">{{ description }}</p>
  <p v-if="constraints" class="fr-text--sm">
    <span>Options acceptées :&#32;</span>
    <span v-for="(item, idx) in constraints" :key="idx">
      <AppCode :content="item" />
      <span v-if="idx < constraints.length - 1">,&#32;</span>
    </span>
  </p>
  <p v-if="multiple" class="fr-text--sm">
    Spécifiez plusieurs options en séparant avec
    <AppCode :content="separator" />
  </p>
</template>
