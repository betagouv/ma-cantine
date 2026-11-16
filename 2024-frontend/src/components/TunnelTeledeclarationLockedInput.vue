<script setup>
defineProps(["value", "label"])
</script>

<template>
  <div class="tunnel-teledeclaration-locked-input">
    <DsfrInput
      :model-value="value"
      :label="label"
      :label-visible="false"
      wrapper-class="fr-input-wrap fr-icon-lock-fill"
      readonly
    />
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

  .fr-icon-lock-fill::before {
    color: var(--text-title-blue-france);
  }
}
</style>
