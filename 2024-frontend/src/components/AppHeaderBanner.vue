<script setup>
const show = window.NOTICE_BANNER_SHOW
</script>

<template>
  <DsfrNotice v-if="show" />
</template>
