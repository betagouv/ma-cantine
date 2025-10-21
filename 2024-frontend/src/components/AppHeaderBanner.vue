<script setup>
const show = window.NOTICE_BANNER_SHOW
const title = window.NOTICE_BANNER_TITLE
</script>

<template>
  <DsfrNotice v-if="show" :title="title" />
</template>
