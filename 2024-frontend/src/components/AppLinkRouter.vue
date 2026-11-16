<script setup>
defineProps(["to", "title", "icon", "isBlank"])
</script>

<template>
  <router-link :to="to" :target="isBlank ? '_blank' : '_self'">
    <span v-if="icon" :class="`${icon} ma-cantine--icon-xs`" aria-hidden="true"></span>
    {{ title }}
    <span v-if="!icon && !isBlank" class="fr-icon-arrow-right-line ma-cantine--icon-xs" aria-hidden="true"></span>
  </router-link>
</template>
