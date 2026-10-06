<script setup>
const contactEmail = window.CONTACT_EMAIL
</script>

<template>
  <a :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
</template>
