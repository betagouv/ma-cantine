<script setup>
import AppLinkRouter from "@/components/AppLinkRouter.vue"
defineProps(["title", "icon", "buttons"])
</script>
<template>
  <div class="import-card fr-card fr-px-4w fr-py-2w">
    <div>
      <div class="import-card__header fr-mb-2w">
        <h2 class="fr-h5 fr-mb-0">{{ title }}</h2>
        <img :src="icon" class="import-card__icon" :alt="`Illustration de ${title}`">
      </div>
      <div v-for="button in buttons" :key="button.label" class="fr-mb-2w">
        <AppLinkRouter :to="button.route" :title="button.label" :icon="button.icon" />
        <p v-if="button.description" class="fr-text--xs fr-mb-0">{{ button.description }}</p>
      </div>
      <DsfrCallout v-if="$slots.callout" class="fr-mb-0">
        <slot name="callout"></slot>
      </DsfrCallout>
    </div>
  </div>
</template>

<style lang="scss">
.import-card {
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__icon {
    width: 4rem;
    height: 4rem;
  }
}
</style>
