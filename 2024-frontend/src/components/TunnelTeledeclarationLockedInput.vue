<script setup>
const props = defineProps(["value", "label"])
</script>

<template>
  <div class="tunnel-teledeclaration-locked-input">
    <DsfrInput
      :model-value="props.value"
      :label="props.label"
      :label-visible="false"
      wrapper-class="fr-input-wrap fr-icon-lock-fill"
      readonly
    />
  </div>
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-locked-input {
  :deep(.fr-input) {
    background-color: white;
    box-shadow: inset 0 -2px 0 0 #e5e5e5;
  }

  :deep(.fr-icon-lock-fill::before) {
    color: var(--text-title-blue-france);
  }
}
</style>
