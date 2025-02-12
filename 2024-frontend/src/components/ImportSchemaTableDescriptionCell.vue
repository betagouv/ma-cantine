<script setup>
import { ref } from "vue"
import AppCode from "@/components/AppCode.vue"
import { useRoute } from "vue-router"

defineOptions({ inheritAttrs: false })
const route = useRoute()
const props = defineProps(["id", "title", "description", "constraints", "multiple", "separator"])
const hash = route.hash.replace("#", "")
const isSelected = ref(hash === props.id)
</script>

<template>
  <p
    :id
    class="import-schema-table-description-cell fr-text--sm fr-mb-1w"
    :class="{
      selected: isSelected,
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

<style lang="scss">
.import-schema-table-description-cell {
  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--text-title-red-marianne);
    opacity: 0;
  }

  &.selected {
    &::before {
      opacity: 0.1;
    }
  }
}
</style>
