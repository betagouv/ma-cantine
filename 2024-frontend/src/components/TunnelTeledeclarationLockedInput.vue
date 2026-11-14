<script setup>
defineProps(["value", "label", "errorMessage"])
</script>

<template>
  <div class="tunnel-teledeclaration-locked-input fr-input-group" :class="{ 'fr-input-group--error': errorMessage }">
    <DsfrInput
      :model-value="value"
      :label="label"
      :label-visible="false"
      :is-invalid="!!errorMessage"
      wrapper-class="fr-input-wrap fr-icon-lock-fill"
      readonly
    />
    <p v-if="errorMessage" class="fr-error-text">{{ errorMessage }}</p>
  </div>
</template>

<style lang="scss">
.tunnel-teledeclaration-locked-input {
  .fr-input {
    background-color: var(--background-default-grey);
    box-shadow: inset 0 -2px 0 0 #e5e5e5;
    pointer-events: none;
    user-select: none;
  }

  &.fr-input-group--error .fr-input {
    box-shadow: inset 0 -2px 0 0 var(--border-plain-error);
  }

  .fr-icon-lock-fill::before {
    color: var(--text-title-blue-france);
  }
}
</style>
