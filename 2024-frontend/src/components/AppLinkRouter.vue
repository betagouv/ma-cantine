<script setup>
defineProps(["to", "title", "icon"])
</script>

<template>
  <router-link :to="to">
    <span v-if="icon" :class="`${icon} ma-cantine--icon-xs`" aria-hidden="true"></span>
    {{ title }}
    <span class="fr-icon-arrow-right-line ma-cantine--icon-xs" aria-hidden="true"></span>
  </router-link>
</template>
