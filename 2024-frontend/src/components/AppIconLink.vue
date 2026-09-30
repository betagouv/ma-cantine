<script setup>
import { computed } from "vue"
const props = defineProps(["bottom"])
const bottomPosition = computed(() => props.bottom || "50%")
</script>

<template>
  <div :aria-hidden="true" class="app-icon-link"></div>
</template>

<style lang="scss">
.app-icon-link {
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    left: 10%;
    bottom: v-bind(bottomPosition);
    width: 1px;
    height: 100%;
    background-color: var(--border-plain-grey);
  }

  &::after {
    content: "";
    position: absolute;
    left: 10%;
    bottom: v-bind(bottomPosition);
    height: 1px;
    width: 80%;
    background-color: var(--border-plain-grey);
  }
}
</style>
