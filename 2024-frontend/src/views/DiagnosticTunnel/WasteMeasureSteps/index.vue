<script setup>
const name = defineModel()
</script>

<template>
  <DsfrInput v-model="name" label="Nom" placeholder="Jean Dupont" label-visible required hint="Indiquez votre nom" />
</template>
