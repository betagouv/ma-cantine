<script setup>
import AppCode from "@/components/AppCode.vue"

defineProps(["id", "title", "description", "constraints", "multiple", "separator"])
defineOptions({ inheritAttrs: false })
</script>

<template>
  <p
    :id
    class="import-schema-table-description-cell import-schema-table-description-cell--selected fr-text--sm fr-mb-1w"
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

  &--selected {
    &::before {
      opacity: 0.1;
    }
  }
}
</style>
