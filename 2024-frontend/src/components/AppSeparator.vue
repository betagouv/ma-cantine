<script setup>
import { computed } from "vue"

const props = defineProps(["orientation"])
const isVertical = computed(() => props.orientation === "vertical")
</script>

<template>
  <hr :aria-hidden="true" class="app-separator" :class="{ 'app-separator--vertical': isVertical }" />
</template>

<style lang="scss">
.app-separator {
  width: 100%;
  height: 1px;
  display: block;
  padding-bottom: 0;
  background-color: var(--border-default-grey);

  &--vertical {
    width: 1px;
    height: auto;
    margin: 0;
  }
}
</style>
