<script setup>
const show = window.SHOW_INFORMATION_BANNER
</script>

<template>
  <DsfrNotice v-if="show" />
</template>
