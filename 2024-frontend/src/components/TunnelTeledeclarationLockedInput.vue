<script setup>
defineProps(["value", "label", "errorMessage"])
</script>

<template>
  <div class="tunnel-teledeclaration-locked-input">
    <DsfrInputGroup
      :model-value="value"
      :label="label"
      :label-visible="false"
      :error-message="errorMessage"
      wrapper-class="fr-mb-0"
      readonly
    />
    <VIcon name="ri-lock-fill" color="var(--text-title-blue-france)" class="tunnel-teledeclaration-locked-input__icon" />
  </div>
</template>

<style lang="scss">
.tunnel-teledeclaration-locked-input {
  position: relative;

  .fr-input {
    margin-top: 0;
    padding-right: 2.5rem;
    background-color: var(--background-default-grey);
    box-shadow: inset 0 -2px 0 0 #e5e5e5;
    pointer-events: none;
    user-select: none;
  }

  .fr-input-group--error .fr-input {
    box-shadow: inset 0 -2px 0 0 var(--border-plain-error);
  }

  &__icon {
    position: absolute;
    top: 1.25rem;
    right: 1rem;
    transform: translateY(-50%);
  }
}
</style>
