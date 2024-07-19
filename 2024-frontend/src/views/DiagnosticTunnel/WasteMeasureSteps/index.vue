<script setup>
defineProps(["stepUrlSlug"])

const name = defineModel()
</script>

<template>
  <div v-if="stepUrlSlug === 'example'">
    <DsfrInput v-model="name" label="Nom" placeholder="Jean Dupont" label-visible required hint="Indiquez votre nom" />
  </div>
  <div v-else-if="stepUrlSlug === 'test'">
    <DsfrInput v-model="name" label="Autre champ" label-visible />
  </div>
  <div v-else>
    <p>Unknown step (shouldn't arrive here)</p>
  </div>
</template>
