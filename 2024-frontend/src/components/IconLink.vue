<script setup>
import { computed } from "vue"
const props = defineProps(["top", "bottom"])

const isFromTop = computed(() => props.top !== undefined && props.top !== null)
const topPositionVertical = computed(() => isFromTop.value ? 0 : "auto")
const bottomPosition = computed(() => isFromTop.value ? "auto" : props.bottom)
const height = computed(() => isFromTop.value ? props.top : "100%")
const topPositionHorizontal = computed(() => isFromTop.value ? props.top : "auto")
</script>

<template>
  <div :aria-hidden="true" class="icon-link"></div>
</template>

<style lang="scss">
.icon-link {
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    left: 10%;
    top: v-bind(topPositionVertical);
    bottom: v-bind(bottomPosition);
    width: 1px;
    height: v-bind(height);
    background-color: var(--border-default-grey);
  }

  &::after {
    content: "";
    position: absolute;
    left: 10%;
    top: v-bind(topPositionHorizontal);
    bottom: v-bind(bottomPosition);
    height: 1px;
    width: 80%;
    background-color: var(--border-default-grey);
  }
}
</style>
