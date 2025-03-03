<script setup>
import { defineProps } from "vue"
defineProps(["to", "title"])
</script>

<template>
  <router-link :to="to">
    {{ title }}
    <span class="fr-icon-arrow-right-line ma-cantine--icon-xs" aria-hidden="true"></span>
  </router-link>
</template>
