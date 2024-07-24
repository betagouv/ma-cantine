<script setup>
import { defineProps } from "vue"

defineProps(["question"])
</script>

<template>
  <!-- TODO: blue border styling and padding -->
  <div>
    <!-- TODO: question icon and styling -->
    <p v-if="question">{{ question }}</p>
    <slot />
  </div>
</template>
