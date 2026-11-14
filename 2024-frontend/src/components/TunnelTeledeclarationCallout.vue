<template>
  <div class="fr-callout tunnel-teledeclaration-callout">
    <slot />
  </div>
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-callout {
  background-image: linear-gradient(0deg, var(--border-default-blue-france), var(--border-default-blue-france));
  background-size: 100% 0.25rem;
  background-position: 0 0;
}
</style>
