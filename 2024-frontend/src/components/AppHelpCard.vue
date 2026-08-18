<script setup>
defineProps(["title", "content"])
</script>

<template>
  <div class="app-help-card fr-card fr-p-7v">
    <div class="app-help-card__content">
      <span class="fr-icon-question-fill fr-text-title--blue-france" aria-hidden="true"></span>
      <div>
        <p class="ma-cantine--bold fr-mb-1w fr-text--lg">
          {{ title }}
        </p>
        <p>{{ content }}</p>
        <div>
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.app-help-card {

  &__content {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    align-items: baseline;
  }
}
</style>
