<script setup>
defineProps(["group"])
const model = defineModel()
</script>

<template>
  <DsfrAccordionsGroup class="fr-mb-5w" v-model="model">
    <h2 class="fr-h5">{{ group.title }}</h2>
    <DsfrAccordion v-for="(accordion, index) in group.accordions" :key="index" :title="accordion.title" title-tag="h3">
      <component v-if="accordion.component" :is="accordion.component"></component>
      <p v-else>{{ accordion.content }}</p>
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>
