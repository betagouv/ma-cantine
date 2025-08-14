<script setup>
defineProps(["warnings"])
</script>

<template>
  <DsfrNotice v-for="warning in warnings" :key="warning" class="fr-my-2w" :title="warning" />
</template>
