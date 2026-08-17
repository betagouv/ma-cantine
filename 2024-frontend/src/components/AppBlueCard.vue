<script setup>
import { useRouter } from 'vue-router'
defineProps(['title', 'button', 'alert'])

const router = useRouter()
const goTo = (to) => {
  router.push({ name: to })
}
</script>

<template>
  <div class="app-blue-card fr-background-alt--blue-france fr-p-4w">
    <p class="fr-h6">{{ title }}</p>
    <DsfrAlert :description="alert" small class="fr-mb-2w" />
    <slot />
    <DsfrButton :label="button.label" @click="goTo(button.to)" secondary />
  </div>
</template>
