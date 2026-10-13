<script setup>
const props = defineProps(["content", "label"])
</script>

<template>
  <span class="app-tooltip-hover">
    <DsfrTooltip :content="props.content" on-hover @click.prevent>
      <span class="fr-icon-information-line" aria-hidden="true"></span>
      <span class="fr-sr-only">{{ props.label || "Infobulle" }}</span>
    </DsfrTooltip>
  </span>
</template>

<style lang="scss">
.app-tooltip-hover {
  display: inline-flex;

  :deep(.fr-link) {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    background-image: none;
  }
}
</style>
