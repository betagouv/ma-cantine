<script setup>
import { computed } from 'vue'

const props = defineProps(["title", "content", "icon", "changeIconColor"])
const iconDisplay = computed(() => props.icon || "fr-icon-question-fill")
const iconDefaultColor = computed(() => props.changeIconColor ? "" : "fr-text-title--blue-france")
</script>

<template>
  <div class="app-help-card fr-card fr-p-7v">
    <div class="app-help-card__content">
      <span :class="`${iconDefaultColor} ${iconDisplay}`" aria-hidden="true"></span>
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
