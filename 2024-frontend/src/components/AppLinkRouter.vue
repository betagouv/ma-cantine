<script setup>
import { computed } from "vue"
const props = defineProps(["to", "title", "icon", "target"])
const displayArrowIcon = computed(() => !props.icon && props.target !== '_blank')
const displayIcon = computed(() => props.icon !== undefined && props.icon !== null)
</script>

<template>
  <router-link :to="props.to" :target="props.target || '_self'">
    <span v-if="displayIcon" :class="`${props.icon} ma-cantine--icon-xs`" aria-hidden="true"></span>
    {{ title }}
    <span v-if="displayArrowIcon" class="fr-icon-arrow-right-line ma-cantine--icon-xs" aria-hidden="true"></span>
  </router-link>
</template>
