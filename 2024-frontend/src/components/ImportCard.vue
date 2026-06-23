<script setup>
import { useRouter } from "vue-router"
defineProps(["title", "icon", "buttons"])

/* Router */
const router = useRouter()
const goTo = (name) => router.push({ name })
</script>
<template>
  <div class="fr-card fr-p-4w">
    <div>
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle fr-grid-row--left fr-mb-2w">
        <img :src="icon" :alt="`Illustration de ${title}`">
        <h2 class="fr-h5 fr-text-title--blue-france fr-mb-0 fr-ml-2w">{{ title }}</h2>
      </div>
      <div v-for="button in buttons" :key="button.label" class="fr-mb-2w">
        <DsfrButton tertiary :label="button.label" :icon="button.icon" @click="goTo(button.route)" />
        <p v-if="button.description" class="fr-text--xs fr-mb-0">{{ button.description }}</p>
      </div>
      <DsfrCallout v-if="$slots.callout" class="fr-mb-0">
        <slot name="callout"></slot>
      </DsfrCallout>
    </div>
  </div>
</template>
