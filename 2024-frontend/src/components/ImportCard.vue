<script setup>
import AppLinkRouter from "@/components/AppLinkRouter.vue"
defineProps(["title", "icon", "buttons"])
</script>
<template>
  <div class="import-card fr-card fr-px-4w fr-py-2w fr-mb-2w" :class="{ 'fr-background-alt--grey': disabled }">
    <div class="import-card__header fr-mb-2w">
      <h2 class="fr-h5 fr-mb-0">
        {{ title }}
        <DsfrBadge v-if="$slots.disabled" type="neutral" label="Non disponible" class="fr-ml-2w" />
      </h2>
      <img :src="icon" class="import-card__icon" :alt="`Illustration de ${title}`">
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12" :class="{ 'fr-col-md-6': $slots.callout }">
        <slot name="disabled"></slot>
        <ul class="ma-cantine--unstyled-list fr-mb-3w">
          <li v-for="button in buttons" :key="button.label" class="fr-mb-1w">
            <AppLinkRouter :to="{name: button.route}" :title="button.label" :icon="button.icon" />
            <p v-if="button.description" class="fr-text--xs fr-mb-0">{{ button.description }}</p>
          </li>
        </ul>
      </div>
      <div class="fr-col-12 fr-col-md-6" v-if="$slots.callout">
        <DsfrCallout class="fr-mb-0">
          <slot name="callout"></slot>
        </DsfrCallout>
      </div>
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
